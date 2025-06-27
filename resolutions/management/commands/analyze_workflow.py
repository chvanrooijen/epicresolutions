from django.core.management.base import BaseCommand
from resolutions.models import Role, Domain, Resolution


class Command(BaseCommand):
    help = 'Display resolution workflow structure and relationships'

    def add_arguments(self, parser):
        parser.add_argument(
            '--role',
            type=str,
            help='Filter by specific role name',
        )
        parser.add_argument(
            '--domain',
            type=str,
            help='Filter by specific domain name',
        )
        parser.add_argument(
            '--show-relationships',
            action='store_true',
            help='Show related resolutions',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== EPIC Resolutions Workflow Structure ===\n'))

        # Filter options
        role_filter = options.get('role')
        domain_filter = options.get('domain')
        show_relationships = options.get('show_relationships')

        # Get all roles
        roles = Role.objects.all().order_by('name')
        if role_filter:
            roles = roles.filter(name__icontains=role_filter)

        for role in roles:
            self.stdout.write(self.style.HTTP_INFO(f'\n🎭 ROLE: {role.name}'))
            
            # Get resolutions for this role
            resolutions = Resolution.objects.filter(role=role).select_related('domain').prefetch_related('related_resolutions')
            
            if domain_filter:
                resolutions = resolutions.filter(domain__name__icontains=domain_filter)

            if not resolutions.exists():
                self.stdout.write('   No resolutions found')
                continue

            # Group by domain
            domains = {}
            for resolution in resolutions:
                domain_name = resolution.domain.name if resolution.domain else 'No Domain'
                if domain_name not in domains:
                    domains[domain_name] = []
                domains[domain_name].append(resolution)

            for domain_name, domain_resolutions in domains.items():
                self.stdout.write(f'   📂 {domain_name}:')
                
                for resolution in domain_resolutions:
                    label = resolution.display_label
                    self.stdout.write(f'      • {label}')
                    
                    if show_relationships:
                        related = resolution.related_resolutions.all()
                        if related.exists():
                            self.stdout.write('        🔗 Related to:')
                            for rel in related:
                                self.stdout.write(f'           → {rel.role.name}: {rel.display_label}')
                        
                        # Show what resolutions point to this one
                        pointing_to_this = Resolution.objects.filter(related_resolutions=resolution)
                        if pointing_to_this.exists():
                            self.stdout.write('        ⬅️  Referenced by:')
                            for ref in pointing_to_this:
                                self.stdout.write(f'           ← {ref.role.name}: {ref.display_label}')

        # Summary statistics
        self.stdout.write(self.style.SUCCESS('\n=== SUMMARY ==='))
        total_roles = Role.objects.count()
        total_domains = Domain.objects.count()
        total_resolutions = Resolution.objects.count()
        consumer_resolutions = Resolution.objects.filter(role__name__icontains='consumer').count()
        
        self.stdout.write(f'Total Roles: {total_roles}')
        self.stdout.write(f'Total Domains: {total_domains}')
        self.stdout.write(f'Total Resolutions: {total_resolutions}')
        self.stdout.write(f'Consumer Resolutions: {consumer_resolutions}')
        
        # Check for resolutions without relationships
        resolutions_without_relationships = Resolution.objects.filter(related_resolutions__isnull=True).exclude(role__name__icontains='consumer')
        if resolutions_without_relationships.exists():
            self.stdout.write(self.style.WARNING(f'\n⚠️  {resolutions_without_relationships.count()} non-consumer resolutions have no relationships'))
            
        self.stdout.write(self.style.SUCCESS('\n✅ Analysis complete!'))
