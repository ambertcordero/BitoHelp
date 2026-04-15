import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bitohelp_api.settings')
django.setup()

from nonprofits.models import Nonprofit
nonprofits_data = [
    {
        'name': 'CARA',
        'description': 'Compassion and Responsibility for Animals — dedicated to animal welfare in the Philippines',
        'bch_address': 'bchtest:qpq3d9hwgq4husnrmshgtv6d3dh5tnsw2s2y6ryy26',
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
        'bch_address': 'bchtest:qz2lq3g5c2ep99n45gddtlagsdfr7ungngqkw73kw2',
        'website': 'https://childhope.org.ph',
        'email': 'info@childhope.org.ph',
        'category': 'children_youth',
        'verified': True,
        'active': True,
    },
    {
        'name': 'Save the Children',
        'description': 'Global nonprofit protecting children and ensuring their right to health, education, and safety',
        'bch_address': 'bchtest:qpjmvz8swz47levf5zdz7y3eas2lcqxx0utd0vuq3g',
        'website': 'https://savethechildren.org.ph',
        'email': 'info@savethechildren.org.ph',
        'category': 'children_youth',
        'verified': True,
        'active': True,
    },
    {
        'name': 'World Vision',
        'description': 'International humanitarian organization focused on child welfare, emergency relief, and community development',
        'bch_address': 'bchtest:qque8pzlpfnas6wgfrun8k8nfq0x9r4rnujfsvvew4',
        'website': 'https://worldvision.org.ph',
        'email': 'info@worldvision.org.ph',
        'category': 'children_youth',
        'verified': True,
        'active': True,
    },
    {
        'name': 'Gawad Kalinga',
        'description': 'Nation-building movement fighting poverty through community development and housing programs',
        'bch_address': 'bchtest:qq8n5g7rxgd93rpgs27tc2q0n0v7qsvmeq9keu9490',
        'website': 'https://gk1world.com',
        'email': 'info@gk1world.com',
        'category': 'housing_humanitarian',
        'verified': True,
        'active': True,
    },
    {
        'name': 'Green Earth',
        'description': 'Environmental conservation and sustainability advocacy organization',
        'bch_address': 'bchtest:qpl3a7u92s0kdpw37ky4y2cwz232kh2hzgalyztp95',
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
