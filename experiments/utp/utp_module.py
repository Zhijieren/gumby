import random

from gumby.experiment import experiment_callback
from gumby.modules.community_launcher import CommunityLauncher
from gumby.modules.experiment_module import static_module
from gumby.modules.community_experiment_module import CommunityExperimentModule
from gumby.modules.isolated_community_loader import IsolatedCommunityLoader

from .utp_community import UTPCommunity


class UTPCommunityLoader(IsolatedCommunityLoader):

    def __init__(self, session_id):
        super(UTPCommunityLoader, self).__init__(session_id)
        self.set_launcher(UTPCommunityLauncher())


class UTPCommunityLauncher(CommunityLauncher):

    def get_community_class(self):
        return UTPCommunity

    def get_kwargs(self, session):
        return {}


@static_module
class UTPModule(CommunityExperimentModule):

    def __init__(self, experiment):
        super(UTPModule, self).__init__(experiment, UTPCommunity)
        self.dispersy_provider.custom_community_loader = UTPCommunityLoader(self.dispersy_provider.session_id)

    @experiment_callback
    def send_to_random(self):
        """
        Request a random signature from one of your known candidates
        """
        known_candidates = list(self.community.dispersy_yield_verified_candidates())
        if known_candidates:
            candidate = random.choice(known_candidates)
            self._logger.info("SENDING DATA TO %s", str(candidate))
            self.community.send_utp_message(candidate, "THIS IS MY DATA")
        else:
            self._logger.info("NO CANDIDATES TO SEND TO")
