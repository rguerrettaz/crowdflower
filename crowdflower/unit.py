# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import
from .base import Attribute, RoAttribute, JobResource, Promise

__author__ = u'Ilja Everilä <ilja.everila@liilak.com>'


class UnitPromise(JobResource, Promise):
    """
    A promise that a :class:`Unit` will be available for querying attributes
    when needed.
    """

    id = RoAttribute()
    data = Attribute()

    def _get_object(self):
        """
        :class:`Unit` getter.
        """
        return self.client.get_unit(self.job, self.id)


class Unit(JobResource):
    """
    CrowdFlower Unit.

    Documentation for attributes can be found at
    http://success.crowdflower.com/customer/portal/articles/1621707 .

    :param job: :class:`~.job.Job` instance owning this :class:`Unit`
    :type job: crowdflower.job.Job
    :param client: :class:`~.client.Client` instance
    :type client: crowdflower.client.Client
    :param data: Unit JSON dictionary
    :type data: dict
    """

    created_at = RoAttribute()
    id = RoAttribute()
    judgments_count = RoAttribute()
    updated_at = RoAttribute()

    agreement = Attribute()
    data = Attribute()
    difficulty = Attribute()
    job_id = Attribute()
    missed_count = Attribute()
    state = Attribute()

    @property
    def results(self):
        """
        Get unit results, if available. RO attribute.
        """
        return self._json.get('results')

    def get_aggregate(self, key, default=None):
        """
        Get aggregated result for ``key``, or return ``default``.

        :param key: Name of result value.
        :type key: str
        :param default: Default value in case the given key is not found.
        """
        try:
            return self._json['results'][key]['agg']

        except KeyError:
            return default
