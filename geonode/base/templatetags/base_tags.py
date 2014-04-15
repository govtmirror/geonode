from django import template

from django.db.models import Count

from agon_ratings.models import Rating
from django.contrib.contenttypes.models import ContentType

from geonode.base.models import Classification, TopicCategory

register = template.Library()

counts = ('map','layer','document')

@register.assignment_tag
def num_ratings(obj):
    ct = ContentType.objects.get_for_model(obj)
    return len(Rating.objects.filter(
                object_id = obj.pk,
                content_type = ct
    ))

@register.assignment_tag
def classifications():
    classifications = Classification.objects.all()
    for c in counts:
        classifications = classifications.annotate(**{ '%s_count' % c : Count('resourcebase__%s__classification' % c)})
    return classifications

@register.assignment_tag
def distribution_restrictions():
    distribution_restrictions = DistributionRestriction.objects.all()
    for c in counts:
        distribution_restrictions = distribution_restrictions.annotate(**{ '%s_count' % c : Count('resourcebase__%s__distribution_restrictions' % c)})
    return distribution_restrictions

@register.assignment_tag
def categories():
    topics = TopicCategory.objects.all()
    for c in counts:
        topics = topics.annotate(**{ '%s_count' % c : Count('resourcebase__%s__category' % c)})
    return topics
    
