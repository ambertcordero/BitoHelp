import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bitohelp_api.settings')
django.setup()

from nonprofits.models import Nonprofit
nonprofits_data = [
    {
        'name': 'CARA',
        'description': 'Compassion and Responsibility for Animals — dedicated to animal welfare in the Philippines',
        'bch_address': 'bchtest:qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy',
        'website': 'https://caraphil.org',
        'email': 'info@caraphil.org',
        'category': 'animals',
        'verified': True,
        'active': True,
    },
    {
        'name': 'Caritas Manila',
        'description': 'Catholic charitable organization serving the poorest communities in Metro Manila',
        'bch_address': 'bchtest:qzprs3rcaqqad6tjtewe28v93y4z0mlmpchrfxdhrk',
        'website': 'https://caritasmanila.org.ph',
        'email': 'info@caritasmanila.org.ph',
        'category': 'poverty',
        'verified': True,
        'active': True,
    },
    {
        'name': 'ChildHope PH',
        'description': 'Empowering street children and urban poor youth through education and community programs',
        'bch_address': 'bchtest:qpwngrc5j8d7vvz0a0mn0z5yak4axf8mvqnkzgd4n8',
        'website': 'https://childhope.org.ph',
        'email': 'info@childhope.org.ph',
        'category': 'children_youth',
        'verified': True,
        'active': True,
    },
    {
        'name': 'Save the Children',
        'description': 'Global nonprofit protecting children and ensuring their right to health, education, and safety',
        'bch_address': 'bchtest:qzj5zu6fgg8v2we82gh76xnrk9njcregluzgaztm45',
        'website': 'https://savethechildren.org.ph',
        'email': 'info@savethechildren.org.ph',
        'category': 'children_youth',
        'verified': True,
        'active': True,
    },
    {
        'name': 'World Vision',
        'description': 'International humanitarian organization focused on child welfare, emergency relief, and community development',
        'bch_address': 'bchtest:qr5agtachyxvrwxu76vzszan5pnvuzy8duhv4lxry',
        'website': 'https://worldvision.org.ph',
        'email': 'info@worldvision.org.ph',
        'category': 'children_youth',
        'verified': True,
        'active': True,
    },
    {
        'name': 'Gawad Kalinga',
        'description': 'Nation-building movement fighting poverty through community development and housing programs',
        'bch_address': 'bchtest:qqfx3wcg8ts09mt5l3zey06wenapyfqq2qrcyj5x0s',
        'website': 'https://gk1world.com',
        'email': 'info@gk1world.com',
        'category': 'housing_humanitarian',
        'verified': True,
        'active': True,
    },
    {
        'name': 'Green Earth',
        'description': 'Environmental conservation and sustainability advocacy organization',
        'bch_address': 'bchtest:qzx35jmyr0fw9e0ffxkdp5qm7s2w5vyuyu67fdnqzk',
        'website': 'https://greenearth.ph',
        'email': 'info@greenearth.ph',
        'category': 'environment',
        'verified': True,
        'active': True,
    },
    {
        'name': 'Haribon Foundation',
        'description': 'Pioneering Philippine biodiversity conservation through science-based advocacy and community engagement',
        'bch_address': 'bchtest:qpm2qsznhks23z7629mms6s4cwef74vcwvy22gdx6a',
        'website': 'https://haribon.org.ph',
        'email': 'info@haribon.org.ph',
        'category': 'environment',
        'verified': True,
        'active': True,
    },
]

def seed_nonprofits():
    print("Replacing all nonprofits...")
    Nonprofit.objects.all().delete()
    print("  Cleared existing nonprofits.")

    for data in nonprofits_data:
        nonprofit = Nonprofit.objects.create(**data)
        print(f"  Created: {nonprofit.name} [{nonprofit.category}]")

    print(f"\n  Total nonprofits: {Nonprofit.objects.count()}")
    print("  Done!")

if __name__ == '__main__':
    seed_nonprofits()
