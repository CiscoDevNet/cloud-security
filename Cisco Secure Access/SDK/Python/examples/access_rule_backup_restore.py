from secure_access.api import access_rules_api
from secure_access.api_client import ApiClient
from access_token import generate_access_token
from secure_access.configuration import Configuration
from secure_access.models import PutRuleRequest
from secure_access.models import AddRuleRequest
import json, argparse, logging, sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler() # Or logging.FileHandler('my_app.log')
logger.addHandler(handler)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)


class AccessRulesBackupAndRestore:
    def __init__(self, offset=None, limit=None, rules=None):
        self.access_token = generate_access_token()
        self.configuration = Configuration(
            access_token=self.access_token,
        )
        self.api_client = ApiClient(configuration=self.configuration)
        self.access_rule_list = []
        self.access_rule_list_response = None
        self.access_rule_response = None
        self.backup_file_name = "rules_backup.json"
        self.offset = offset
        self.limit = limit
        self.rules = rules


    def put_access_rule_request(self, access_rule):
        return PutRuleRequest.from_dict(access_rule)

    def update_access_rule(self, rule_id, access_rule_request):
        api_instance = access_rules_api.AccessRulesApi(api_client=self.api_client)
        try:
            self.access_rule_response = api_instance.put_rule_without_preload_content(rule_id, access_rule_request)
        except Exception as e:
            logger.error("An error occurred while updating the access rule:", e)

    def create_access_rule_request(self, access_rule):
        return AddRuleRequest.from_dict(access_rule)

    def create_access_rule(self, access_rule_request):
        api_instance = access_rules_api.AccessRulesApi(api_client=self.api_client)
        try:
            self.access_rule_response = api_instance.add_rule_without_preload_content(access_rule_request)
        except Exception as e:
            logger.error("An error occurred while creating the access rule:", e)

    def list_access_rules(self):
        api_instance = access_rules_api.AccessRulesApi(api_client=self.api_client)
        try:
            if self.offset != None and self.limit != None:
                self.access_rule_list_response = api_instance.list_rules_without_preload_content(
                    offset=self.offset,
                    limit=self.limit)
            elif self.rules:
                self.access_rule_list_response = api_instance.list_rules_without_preload_content(
                    offset=self.offset,
                    limit=self.limit)
            else:
                self.access_rule_list_response = api_instance.list_rules_without_preload_content()
        except Exception as e:
            logger.error("An error occurred while listing acesss rule:", e)

    def get_access_rules(self, id: int):
        api_instance = access_rules_api.AccessRulesApi(api_client=self.api_client)
        try:
            self.access_rule_response = api_instance.get_rule_without_preload_content(id)
        except Exception as e:
            logger.error("An error occurred while fetching an access rule:", e)

    def get_rule_settings_conditions(self):
        self.access_rule_list = self.access_rule_list_response.json()["results"]
        for index, result in enumerate(self.access_rule_list):
            #logger.debug(f"Fetching rule setting and connection for Rule Name: {result.get("ruleName")},Rule Priority: {result.get("rulePriority")} and Rule ID: {result.get("ruleId")}")
            logger.debug("Fetching rule setting and connection for Rule Name: "+result.get("ruleName")+"Rule Priority: "+str(result.get("rulePriority"))+" and Rule ID: "+str(result.get("ruleId"))+"")
            self.get_access_rules(result["ruleId"])
            if self.access_rule_response.status == 200:
                self.access_rule_list[index]["ruleSettings"] = self.access_rule_response.json().get("ruleSettings")
                self.access_rule_list[index]["ruleConditions"] = self.access_rule_response.json().get("ruleConditions")
            else:
                self.access_rule_list[index]["ruleSettings"] = []
                self.access_rule_list[index]["ruleConditions"] = []

    def backup_access_rule_list(self):
        with open(self.backup_file_name, "w+") as rules:
            json.dump(self.access_rule_list, rules, indent=4)

    def parse_backup_access_rules(self):
        try:
            with open(self.backup_file_name, "r+") as rules:
                self.access_rule_list = json.load(rules)
        except Exception as e:
            #logger.error(f"The backup file not found, Please run backup first: {e}")
            logger.error("The backup file not found, Please run backup first: ", e)
            sys.exit(1)

    def restore_access_rules(self):
        if not self.access_rule_list:
            #logger.info(f"No rules are identified to be backed up.")
            logger.info("No rules are identified to be backed up.")
            sys.exit(0)

        for access_rule in self.access_rule_list:
            access_rule_request = self.put_access_rule_request(access_rule)
            #access_rule["rulePriority"] += 2
            #access_rule["ruleName"] = f"{access_rule["ruleName"]} Copy"
            self.update_access_rule(access_rule["ruleId"], access_rule_request)
            if self.access_rule_response.status == 200:
                #logger.debug(f"Rule Name: {access_rule.get("ruleName")}, Rule Priority: {access_rule.get("rulePriority")} and Rule ID: {access_rule.get("ruleId")} is restored")
                #logger.debug("Fetching rule setting and connection for Rule Name: ",access_rule.get("ruleName"), "Rule Priority: ", access_rule.get("rulePriority")," and Rule ID: ", access_rule.get("ruleId"))
                logger.debug("Restored Successfully for Rule ID: "+str(access_rule.get("ruleId"))+"")
            elif self.access_rule_response.status == 404:
                logger.info("The requested RuleId does not exists. Creating the new Rule Access")
                access_rule_request = self.create_access_rule_request(access_rule)
                self.create_access_rule(access_rule_request)
                if self.access_rule_response.status == 200:
                    logger.debug("Created Successfully for Rule ID: "+str(access_rule.get("ruleId"))+"")
                #logger.error(f"Error in restoring the access rule for Rule Name: {access_rule.get("ruleName")},Rule Priority: {access_rule.get("rulePriority")} and Rule ID: {access_rule.get("ruleId")}")
                #logger.error("Error in restoring the access rule for Rule Name: ", access_rule.get("ruleName"), "Rule Priority: ", str(access_rule.get("rulePriority")), " and Rule ID: ", str(access_rule.get("ruleId")))
            else:
                logger.error("Error in restoring the access rule for Rule Name: "+str(access_rule.get("ruleName"))+"Rule Priority: "+str(access_rule.get("rulePriority"))+" and Rule ID: "+str(access_rule.get("ruleId"))+"")

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="Utility to backup and restore access rules")

    #Adding optional parameters
    parser.add_argument('-t',
                        '--type',
                        help="Type of the operation to be performed i.e. either backup or restore the access rules.",
                        required=True,
                        choices=["backup", "restore"],
                        type=str)

    parser.add_argument('-o',
                        '--offset',
                        help="Starting offset to fetch the access rules",
                        required=False,
                        type=int)
    
    parser.add_argument('-l',
                        '--limit',
                        help="limit to fetch the access rules in a call",
                        required=False,
                        type=int)

    parser.add_argument('-r',
                        '--rules',
                        help="list of rule id's to filter the Access Rules",
                        required=False,
                        type=int,
                        nargs="+")

    #Parsing the argument
    args=parser.parse_args()

    logger.info("start of the application.")

    isListRules = False

    if args.type == "backup":
        if args.offset != None and args.limit !=None:
            access_rule = AccessRulesBackupAndRestore(offset = args.offset,
                                                      limit = args.limit)
            isListRules = True
        elif args.rules:
            access_rule = AccessRulesBackupAndRestore(rules = args.rules)
        else:
            access_rule = AccessRulesBackupAndRestore()
            isListRules = True

        if isListRules:
            logger.info("Fetching all the access rules calling rules API.")
            access_rule.list_access_rules()
            if access_rule.access_rule_list_response.status == 200:
                logger.info("Adding rule settings and conditions.")
                logger.debug(access_rule.access_rule_list_response.json().get("count"))
                access_rule.get_rule_settings_conditions()
            else:
                #logger.error(f"Error in fetching the access_rule_list_response")
                logger.error("Error in fetching the access_rule_list_response")
                sys.exit(1)
        else:
            logger.info("Fetching all the rules with RuleId.")
            for rule_id in access_rule.rules:
                access_rule.get_access_rules(rule_id)
                if access_rule.access_rule_response.status == 200:
                    access_rule.access_rule_list.append(access_rule.access_rule_response.json())
                else:
                    #logger.error(f"Error in fetching the access_rule_list_response")
                    logger.error("Error in fetching the access_rule_list_response")
                    sys.exit(1)

        logger.info("Taking backup of all the rules.")
        access_rule.backup_access_rule_list()
    elif args.type == "restore":
        access_rule = AccessRulesBackupAndRestore()
        logger.info("Parsing backed up access rules.")
        access_rule.parse_backup_access_rules()
        logger.info("Restoring the access rules.")
        access_rule.restore_access_rules()
        logger.info("Access Rules restoration is completed.")
