from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from hfc.fabric import Client

class CrossDistSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(CrossDistSwitch, self).__init__(*args, **kwargs)
        self.fabric_client = Client(net_profile="network.yaml")
        self.user = self.fabric_client.get_user('Org1', 'Admin')
        self.channel = self.fabric_client.new_channel('mychannel')

    def invoke_cross_dist_block(self, function_name, args):
        try:
            response = self.fabric_client.chaincode_invoke(
                requestor=self.user,
                channel_name='mychannel',
                peer_names=['peer0.org1.example.com'],
                args=args,
                cc_name='cross_dist_block_chaincode',
                fcn=function_name
            )
            self.logger.info(f"Invoke Response: {response}")
            return response
        except Exception as e:
            self.logger.error(f"Failed to invoke Cross_Dist_Block: {e}")
            return None

    def query_cross_dist_block(self, function_name, args):
        try:
            response = self.fabric_client.chaincode_query(
                requestor=self.user,
                channel_name='mychannel',
                peer_names=['peer0.org1.example.com'],
                args=args,
                cc_name='cross_dist_block_chaincode',
                fcn=function_name
            )
            self.logger.info(f"Query Response: {response}")
            return response
        except Exception as e:
            self.logger.error(f"Failed to query Cross_Dist_Block: {e}")
            return None

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, MAIN_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Example: Register the switch in Cross_Dist_Block when it connects
        switch_id = str(datapath.id)
        switch_details = "Domain-1-Switch"
        self.invoke_cross_dist_block('registerSwitch', [switch_id, switch_details])

        # Query cross-domain flow policies from Cross_Dist_Block
        cross_domain_policy = self.query_cross_dist_block('getFlowPolicy', [switch_id])
        self.logger.info(f"Cross-Domain Policy for Switch {switch_id}: {cross_domain_policy}")

        # Add a default flow to the switch
        self.add_default_flow(datapath)

    def add_default_flow(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)
