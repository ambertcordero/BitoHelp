import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bitohelp_api.settings')
django.setup()

from nonprofits.models import Nonprofit

nonprofits_data = [
    {
        'name': 'Typhoon Relief Fund',
        'description': 'Providing emergency relief and support to typhoon victims across the Philippines',
        'bch_address': 'qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy',
        'website': 'https://typhoonrelief.org',
        'email': 'contact@typhoonrelief.org',
        'category': 'disaster_relief',
        'verified': True,
        'active': True,
    },
    {
        'name': 'Educational Fund',
        'description': 'Supporting education for underprivileged children through scholarships and school supplies',
        'bch_address': 'qp4aadjrpu73d2wxwkxkcrt6gqxgu6a7usxfm96fst',
        'website': 'https://educationfund.org',
        'email': 'info@educationfund.org',
        'category': 'education',
        'verified': True,
        'active': True,
    },
    {
        'name': 'Medical Fund',
        'description': 'Providing medical assistance and healthcare services to communities in need',
        'bch_address': 'qpwngrc5j8d7vvz0a0mn0z5yak4axf8mvqnkzgd4n8',
        'website': 'https://medicalfund.org',
        'email': 'help@medicalfund.org',
        'category': 'health',
        'verified': True,
        'active': True,
    },
    {
        'name': 'Health Fund',
        'description': 'Promoting health and wellness programs for marginalized communities',
        'bch_address': 'qzj5zu6fgg8v2we82gh76xnrk9njcregluzgaztm45',
        'website': 'https://healthfund.org',
        'email': 'contact@healthfund.org',
        'category': 'health',
        'verified': True,
        'active': True,
    },
    {
        'name': 'Environmental Protection Initiative',
        'description': 'Protecting and preserving natural resources and wildlife habitats',
        'bch_address': 'qr5agtachyxvrwxu76vzszan5pnvuzy8duhv4lxry',
        'website': 'https://enviprotect.org',
        'email': 'info@enviprotect.org',
        'category': 'environment',
        'verified': True,
        'active': True,
    },
    {
        'name': 'Clean Water Project',
        'description': 'Providing access to clean drinking water in rural communities',
        'bch_address': 'qqfx3wcg8ts09mt5l3zey06wenapyfqq2qrcyj5x0s',
        'website': 'https://cleanwaterproject.org',
        'email': 'support@cleanwaterproject.org',
        'category': 'environment',
        'verified': True,
        'active': True,
    },
    {
        'name': 'Food Security Alliance',
        'description': 'Fighting hunger and malnutrition through food distribution programs',
        'bch_address': 'qzx35jmyr0fw9e0ffxkdp5qm7s2w5vyuyu67fdnqzk',
        'website': 'https://foodsecurity.org',
        'email': 'contact@foodsecurity.org',
        'category': 'poverty',
        'verified': True,
        'active': True,
    },
    {
        'name': 'Animal Welfare Society',
        'description': 'Rescuing and caring for abandoned and abused animals',
        'bch_address': 'qpm2qsznhks23z7629mms6s4cwef74vcwvy22gdx6a',
        'website': 'https://animalwelfare.org',
        'email': 'rescue@animalwelfare.org',
        'category': 'animal_welfare',
        'verified': True,
        'active': True,
    },
]

def seed_nonprofits():
    print("Seeding nonprofits database...")
    
    created_count = 0
    skipped_count = 0
    
    for data in nonprofits_data:
        existing = Nonprofit.objects.filter(bch_address=data['bch_address']).first()
        
        if existing:
            print(f"  Skipped: {data['name']} (already exists)")
            skipped_count += 1
        else:
            nonprofit = Nonprofit.objects.create(**data)
            print(f" Created: {nonprofit.name}")
            created_count += 1
    
    print(f"\n Summary:")
    print(f"   Created: {created_count}")
    print(f"   Skipped: {skipped_count}")
    print(f"   Total nonprofits in database: {Nonprofit.objects.count()}")
    print("\n Database seeding complete!")

if __name__ == '__main__':
    seed_nonprofits()
