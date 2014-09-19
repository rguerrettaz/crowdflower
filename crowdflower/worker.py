# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import
from inspect import getcallargs
from .base import RoAttribute, JobResource
from functools import wraps, partial

__author__ = u'Ilja Everilä <ilja.everila@liilak.com>'


def _command(f, method='post'):
    """
    Helper function for handling :py:class:`Worker <crowdflower.worker.Worker>` commands.
    """

    @wraps(f)
    def cmd(self, *args, **kwgs):
        """
        Self is :py:class:`crowdflower.worker.Worker` instance.
        """
        callargs = getcallargs(f, self, *args, **kwgs)
        del callargs['self']

        self._client.send_worker_command(
            self,
            f.__name__, callargs,
            method
        )

    return cmd

# TODO: check which is correct:
# ruby-crowdflower Worker or
# http://success.crowdflower.com/customer/portal/articles/1553902-api-request-examples#header_4
_put_command = partial(_command, method='put')


class Worker(JobResource):
    """
    CrowdFlower Worker.

    :param job: :py:class:`Job <crowdflower.job.Job>` instance owning this Worker
    :type job: crowdflower.job.Job
    :param client: API :py:class:`client <crowdflower.client.Client>`
    :type client: crowdflower.client.Client
    :param data: Attributes
    :type data: dict
    """

    id = RoAttribute()

    @_command
    def bonus(self, amount, reason=None):
        """
        Pay Worker a bonus of ``amount`` cents. Optionally
        include a message stating the ``reason`` of the bonus.

        :param amount: Amount in cents
        :type amount: int
        :param reason: Include a message with the bonus
        :type reason: str
        """

    @_command
    def notify(self, message):
        """
        Notify a Worker contributor with the ``message``. The message
        appears in the workers dashboard.

        :param message: Message to Worker
        :type message: str
        """

    @_put_command
    def flag(self, flag, persist=False):
        """
        Flags and prevents a Worker from completing the Job with
        the reason ``flag``. Existing Judgments will not be thrown
        away. If ``persist`` is se to ``True``, then the Worker is
        flagged out from all Jobs.

        :param flag: Flag reason
        :type flag: str
        :param persist: If True, flag in all Jobs (default False)
        :type persist: bool
        """

    @_put_command
    def deflag(self, deflag):
        """
        De-flags a worker with the reason ``deflag``.

        :param deflag: De-flag reason
        :type deflag: str
        """

    @_put_command
    def reject(self):
        """
        Prevents Worker from completing Jobs and removes all Judgments.

        Care should be taken since a finalized Job cannot collect new
        Judgments to replace the missing data.

        This feature is only available to Pro and Enterprise users.
        """