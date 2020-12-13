import socket
import asyncio
import time
import random
import json
import boto3
import botocore
from botocore.config import Config

from walkoff_app_sdk.app_base import AppBase

class AWSEC2(AppBase):
    __version__ = "1.0.0"
    app_name = "AWS ec2"  

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    async def auth_ec2(self, access_key, secret_key, region):
        my_config = Config(
            region_name = region,
            signature_version = 'v4',
            retries = {
                'max_attempts': 10,
                'mode': 'standard'
            },
        )

        self.ec2 = boto3.resource(
            'ec2', 
            config=my_config, 
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

        return self.ec2

    # Write your data inside this function
    async def create_acl_entry(self, access_key, secret_key, region, ACL_id, cidr_block, dryrun, egress, portrange_from, portrange_to, protocol, rule_action, rule_number):
        self.ec2 = await self.auth_ec2(access_key, secret_key, region)

        network_acl = self.ec2.NetworkAcl(ACL_id)
        if protocol.lower() == "tcp":
            protocol = "6"
        elif protocol.lower() == "udp":
            protocol = "17"

        if egress.lower() == "false":
            egress = False
        else:
            egress = True

        if dryrun.lower() == "false":
            dryrun = False
        else:
            dryrun = True

        try:
            return network_acl.create_entry(
                CidrBlock=cidr_block,
                DryRun=dryrun,
                Egress=egress,
                IcmpTypeCode={
                    'Code': 123,
                    'Type': 123
                },
                PortRange={
                    'From': int(portrange_from),
                    'To': int(portrange_to)
                },
                Protocol=protocol,
                RuleAction=rule_action,
                RuleNumber=int(rule_number),
            )
        except botocore.exceptions.ClientError as e:
            print("Error: %s" % e)
            return e


if __name__ == "__main__":
    asyncio.run(AWSEC2.run(), debug=True)
