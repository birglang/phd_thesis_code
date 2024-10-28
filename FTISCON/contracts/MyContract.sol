pragma solidity >=0.4.22 <0.9.0;

contract MyContract{
    
    struct Controller{
        uint256 id;
        string name;
        string ip_address;
    }


    struct Flow_info{
        uint rule_id;
        string src_mac;
        string dst_mac;
        uint priority;
        uint outport;
    }

    struct Switch{
        uint256 id;
        string name;
        string ip_address;
        uint rule_count;
        mapping(uint => Flow_info) rules;
    }
    
        
    mapping(uint => Controller) public controllers;
    mapping(uint => Switch) public switches;

    
    uint public controller_count = 0;
    uint public switch_count = 0;
    uint public rule_count = 0;
    

    function addController(string memory _name, string memory _ip_address ) public{
        controller_count++;
        controllers[controller_count] = Controller(switch_count, _name, _ip_address);
    }
    
    function addSwitches(uint switch_id, string memory _name, string memory _ip_address ) public{
        switch_count++;
                
        switches[switch_id].id = switch_id;
        switches[switch_id].name = _name;
        switches[switch_id].ip_address = _ip_address;
        switches[switch_id].rule_count = 0;
    }
    
    
    function addRule(string memory _src_mac, string memory _dst_mac, uint _priority, uint _outport, uint _switch_id) public{
        switches[_switch_id].rule_count++; 
        switches[_switch_id].rules[switches[_switch_id].rule_count] = Flow_info(switches[_switch_id].rule_count, _src_mac, _dst_mac, _priority, _outport);
    }
    
    function getRules(uint _switch_id, uint _rule_id) view public returns (uint, string memory, string memory, uint, uint) {
        return (switches[_switch_id].rules[_rule_id].rule_id, switches[_switch_id].rules[_rule_id].src_mac, switches[_switch_id].rules[_rule_id].dst_mac, switches[_switch_id].rules[_rule_id].priority, switches[_switch_id].rules[_rule_id].outport);
    }

    function getRuleCount(uint _switch_id) view public returns(uint){
        return switches[_switch_id].rule_count;
    }




    /*
    function verifyFlowRules(uint _switch_id, uint _rule_id, string memory _SRC, string memory _DST, uint _priority, uint _OUTPORT) view public returns (uint) {
        uint status = 0;

        
        string src = switches[_switch_id].rules[_rule_id].src_mac;
        string dst = switches[_switch_id].rules[_rule_id].dst_mac;
        string priority = switches[_switch_id].rules[_rule_id].priority;
        uint outport = switches[_switch_id].rules[_rule_id].outport;

        // check the similarity

        if src == _SRC && dst == _DST && outport == _OUTPORT && priority == _priority {
            return 1;
        }
        else{
            return 0;
        }
    }
    */

    
}
