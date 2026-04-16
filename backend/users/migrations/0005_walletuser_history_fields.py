from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_walletuser_balance_walletuser_chain_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            DO $$
            BEGIN
                -- ───────────────────────────────────────────────────
                -- CASE 1: Broken state — columns renamed to plural
                --         AND converted to jsonb arrays.
                -- ───────────────────────────────────────────────────
                IF EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_name = 'users_walletuser'
                      AND column_name = 'display_names'
                      AND data_type = 'jsonb'
                ) THEN
                    -- Create the history columns from the existing jsonb arrays
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'users_walletuser' AND column_name = 'names_history'
                    ) THEN
                        ALTER TABLE users_walletuser
                            ADD COLUMN names_history jsonb NOT NULL DEFAULT '[]'::jsonb;
                    END IF;
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'users_walletuser' AND column_name = 'emails_history'
                    ) THEN
                        ALTER TABLE users_walletuser
                            ADD COLUMN emails_history jsonb NOT NULL DEFAULT '[]'::jsonb;
                    END IF;
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'users_walletuser' AND column_name = 'contacts_history'
                    ) THEN
                        ALTER TABLE users_walletuser
                            ADD COLUMN contacts_history jsonb NOT NULL DEFAULT '[]'::jsonb;
                    END IF;

                    -- Copy array data into history columns
                    UPDATE users_walletuser SET
                        names_history    = COALESCE(display_names, '[]'::jsonb),
                        emails_history   = COALESCE(emails,        '[]'::jsonb),
                        contacts_history = COALESCE(contacts,      '[]'::jsonb);

                    -- Recreate the original varchar columns
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'users_walletuser' AND column_name = 'display_name'
                    ) THEN
                        ALTER TABLE users_walletuser
                            ADD COLUMN display_name varchar(255) NOT NULL DEFAULT '';
                        -- Extract first element of the array as the current value
                        UPDATE users_walletuser
                            SET display_name = COALESCE(
                                display_names->>0, ''
                            );
                    END IF;
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'users_walletuser' AND column_name = 'email'
                    ) THEN
                        ALTER TABLE users_walletuser
                            ADD COLUMN email varchar(254) NOT NULL DEFAULT '';
                        UPDATE users_walletuser
                            SET email = COALESCE(emails->>0, '');
                    END IF;
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'users_walletuser' AND column_name = 'contact'
                    ) THEN
                        ALTER TABLE users_walletuser
                            ADD COLUMN contact varchar(50) NOT NULL DEFAULT '';
                        UPDATE users_walletuser
                            SET contact = COALESCE(contacts->>0, '');
                    END IF;

                    -- Drop the wrongly-named jsonb columns
                    ALTER TABLE users_walletuser DROP COLUMN IF EXISTS display_names;
                    ALTER TABLE users_walletuser DROP COLUMN IF EXISTS emails;
                    ALTER TABLE users_walletuser DROP COLUMN IF EXISTS contacts;

                -- ───────────────────────────────────────────────────
                -- CASE 2: Columns were only renamed (still varchar).
                -- ───────────────────────────────────────────────────
                ELSIF EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_name = 'users_walletuser'
                      AND column_name = 'display_names'
                ) THEN
                    ALTER TABLE users_walletuser RENAME COLUMN display_names TO display_name;
                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'users_walletuser' AND column_name = 'emails'
                    ) THEN
                        ALTER TABLE users_walletuser RENAME COLUMN emails TO email;
                    END IF;
                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'users_walletuser' AND column_name = 'contacts'
                    ) THEN
                        ALTER TABLE users_walletuser RENAME COLUMN contacts TO contact;
                    END IF;

                    -- Add history columns
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'users_walletuser' AND column_name = 'names_history'
                    ) THEN
                        ALTER TABLE users_walletuser
                            ADD COLUMN names_history jsonb NOT NULL DEFAULT '[]'::jsonb;
                    END IF;
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'users_walletuser' AND column_name = 'emails_history'
                    ) THEN
                        ALTER TABLE users_walletuser
                            ADD COLUMN emails_history jsonb NOT NULL DEFAULT '[]'::jsonb;
                    END IF;
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'users_walletuser' AND column_name = 'contacts_history'
                    ) THEN
                        ALTER TABLE users_walletuser
                            ADD COLUMN contacts_history jsonb NOT NULL DEFAULT '[]'::jsonb;
                    END IF;

                -- ───────────────────────────────────────────────────
                -- CASE 3: Clean state — just add history columns.
                -- ───────────────────────────────────────────────────
                ELSE
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'users_walletuser' AND column_name = 'names_history'
                    ) THEN
                        ALTER TABLE users_walletuser
                            ADD COLUMN names_history jsonb NOT NULL DEFAULT '[]'::jsonb;
                    END IF;
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'users_walletuser' AND column_name = 'emails_history'
                    ) THEN
                        ALTER TABLE users_walletuser
                            ADD COLUMN emails_history jsonb NOT NULL DEFAULT '[]'::jsonb;
                    END IF;
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'users_walletuser' AND column_name = 'contacts_history'
                    ) THEN
                        ALTER TABLE users_walletuser
                            ADD COLUMN contacts_history jsonb NOT NULL DEFAULT '[]'::jsonb;
                    END IF;
                END IF;
            END $$;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),

        # Seed history from scalar fields (for cases 2 & 3 where data wasn't copied)
        migrations.RunSQL(
            sql="""
            UPDATE users_walletuser
            SET names_history = jsonb_build_array(display_name)
            WHERE display_name IS NOT NULL AND display_name != ''
              AND names_history = '[]'::jsonb;

            UPDATE users_walletuser
            SET emails_history = jsonb_build_array(email)
            WHERE email IS NOT NULL AND email != ''
              AND emails_history = '[]'::jsonb;

            UPDATE users_walletuser
            SET contacts_history = jsonb_build_array(contact)
            WHERE contact IS NOT NULL AND contact != ''
              AND contacts_history = '[]'::jsonb;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
