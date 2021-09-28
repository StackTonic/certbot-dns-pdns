import logging

import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common
import powerdns

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for PDNS

    This Authenticator uses the PDNS API to fulfill a dns-01 challenge.
    """

    description = "Obtain certs using a DNS TXT record (if you are using PowerDNS for nameservers)."

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None
        self.pdns = None

    @classmethod
    def add_parser_arguments(cls, add):
        super(Authenticator, cls).add_parser_arguments(add)
        add("credentials", help="PDNS credentials INI file.")

    def more_info(self):
        return "This plugin configures a DNS TXT record to respond to a dns-01 challenge using the PDNS API."

    def _setup_credentials(self):
        self.credentials = self._configure_credentials("credentials", "PDNS credentials INI file", {
            "api": "API Address",
            "key": "API key for Vultr account"
        })

    def _perform(self, domain, validation_name, validation):
        zone = self._get_pdns_client().servers[0].get_zone(domain)
        comments = [powerdns.Comment("dns-01 challange", "cerbot")]
        relative_record_name = self.get_relative_record_name(domain_name, validation_name)
        zone.create_records([
            powerdns.RRSet(relative_record_name, 'TXT', [(validation, False)],comments=comments)
        ])

    def _cleanup(self, domain, validation_name, validation):
        zone = self._get_pdns_client().servers[0].get_zone(domain)
        relative_record_name = self.get_relative_record_name(domain_name, validation_name)
        zone.delete_records([
                powerdns.RRSet(relative_record_name, 'TXT', [(validation, False)]),
        ])

    def _get_pdns_client(self):
        if self.pdns is None:
            api_client = powerdns.PDNSApiClient(api_endpoint=self.credentials.conf("api"), api_key=self.credentials.conf("key"))
            self.pdns = powerdns.PDNSEndpoint(api_client)

        return self.pdns
    def get_relative_record_name(self, base_domain_name, absolute_record_name):
        return absolute_record_name[:-len("." + base_domain_name)]