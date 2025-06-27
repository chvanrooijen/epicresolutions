from django.core.management.base import BaseCommand
from resolutions.models import Role, Domain, Cause, Resolution


class Command(BaseCommand):
    help = 'Set up sample data for the new workflow'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating sample data',
        )

    def handle(self, *args, **options):
        if options.get('clear'):
            self.stdout.write('Clearing existing data...')
            Resolution.objects.all().delete()
            Domain.objects.all().delete()
            Cause.objects.all().delete()
            Role.objects.all().delete()

        self.stdout.write('Creating sample data for new workflow...')

        # Create Roles
        consumer_role, _ = Role.objects.get_or_create(name='Consumer')
        employer_role, _ = Role.objects.get_or_create(name='Employer')
        government_role, _ = Role.objects.get_or_create(name='Government')
        educator_role, _ = Role.objects.get_or_create(name='Educator')

        # Create Domains
        transport_domain, _ = Domain.objects.get_or_create(name='Transportation')
        food_domain, _ = Domain.objects.get_or_create(name='Food')
        energy_domain, _ = Domain.objects.get_or_create(name='Energy')
        waste_domain, _ = Domain.objects.get_or_create(name='Waste')

        # Create Causes
        climate_cause, _ = Cause.objects.get_or_create(name='Climate Change')
        health_cause, _ = Cause.objects.get_or_create(name='Public Health')
        sustainability_cause, _ = Cause.objects.get_or_create(name='Sustainability')

        # Create Consumer Resolutions
        consumer_transport, _ = Resolution.objects.get_or_create(
            role=consumer_role,
            domain=transport_domain,
            label='Use Public Transit',
            positive_action='use public transportation',
            trigger='when commuting to work',
            goal='reduce carbon emissions',
            incentive='save money on gas',
            negative_action='driving alone'
        )
        consumer_transport.causes.add(climate_cause, sustainability_cause)

        consumer_food, _ = Resolution.objects.get_or_create(
            role=consumer_role,
            domain=food_domain,
            label='Buy Local Produce',
            positive_action='buy locally sourced food',
            trigger='when grocery shopping',
            goal='support local farmers',
            incentive='get fresher food',
            negative_action='buying imported produce'
        )
        consumer_food.causes.add(sustainability_cause, health_cause)

        consumer_energy, _ = Resolution.objects.get_or_create(
            role=consumer_role,
            domain=energy_domain,
            label='Use Renewable Energy',
            positive_action='switch to renewable energy',
            trigger='when choosing energy provider',
            goal='reduce fossil fuel dependence',
            incentive='lower long-term costs',
            negative_action='using fossil fuel energy'
        )
        consumer_energy.causes.add(climate_cause, sustainability_cause)

        # Create Related Resolutions for Other Roles
        employer_transport, _ = Resolution.objects.get_or_create(
            role=employer_role,
            domain=transport_domain,
            label='Provide Transit Benefits',
            positive_action='offer public transit subsidies',
            trigger='when developing employee benefits',
            goal='encourage sustainable commuting',
            incentive='reduce parking costs',
            negative_action='only providing parking spaces'
        )
        employer_transport.causes.add(climate_cause, sustainability_cause)
        employer_transport.related_resolutions.add(consumer_transport)

        government_transport, _ = Resolution.objects.get_or_create(
            role=government_role,
            domain=transport_domain,
            label='Improve Public Transit',
            positive_action='invest in public transportation infrastructure',
            trigger='when planning city budgets',
            goal='provide accessible transport options',
            incentive='reduce traffic congestion',
            negative_action='only investing in road infrastructure'
        )
        government_transport.causes.add(climate_cause, sustainability_cause)
        government_transport.related_resolutions.add(consumer_transport)

        educator_food, _ = Resolution.objects.get_or_create(
            role=educator_role,
            domain=food_domain,
            label='Teach Sustainable Agriculture',
            positive_action='include sustainable farming in curriculum',
            trigger='when developing course content',
            goal='educate about local food systems',
            incentive='prepare students for green jobs',
            negative_action='ignoring environmental impact of food'
        )
        educator_food.causes.add(sustainability_cause, health_cause)
        educator_food.related_resolutions.add(consumer_food)

        government_energy, _ = Resolution.objects.get_or_create(
            role=government_role,
            domain=energy_domain,
            label='Renewable Energy Incentives',
            positive_action='provide tax credits for renewable energy',
            trigger='when setting energy policy',
            goal='accelerate clean energy adoption',
            incentive='create green jobs',
            negative_action='subsidizing fossil fuels'
        )
        government_energy.causes.add(climate_cause, sustainability_cause)
        government_energy.related_resolutions.add(consumer_energy)

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write(f'Created {Role.objects.count()} roles')
        self.stdout.write(f'Created {Domain.objects.count()} domains')
        self.stdout.write(f'Created {Cause.objects.count()} causes')
        self.stdout.write(f'Created {Resolution.objects.count()} resolutions')
        
        # Show relationship summary
        consumer_resolutions = Resolution.objects.filter(role=consumer_role)
        self.stdout.write(f'\nConsumer resolutions with relationships:')
        for res in consumer_resolutions:
            related_count = Resolution.objects.filter(related_resolutions=res).count()
            self.stdout.write(f'  • {res.display_label}: {related_count} related resolutions')

        self.stdout.write(self.style.SUCCESS('\n✅ Setup complete! You can now test the workflow.'))
