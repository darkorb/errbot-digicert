import requests
from errbot import BotPlugin, botcmd

class DigiCert(BotPlugin):
    """DigiCert tools for lookups"""

    def get_configuration_template(self):
        """Configuration Options"""
        config = {
            'APIKEY': None
        }
        return config

    @botcmd
    def certsearch(self, msg, args):
        headers = {'X-DC-DEVKEY':self.config['APIKEY']}
        data = requests.get('https://www.digicert.com/services/v2/order/certificate/' + args.strip(), headers=headers)
        if data.status_code != 200:
            return 'Oh dear, something went wrong with the HTTP request (error %s)' % (data.status_code)
        else:
            try:
                self.send_card(title='Details for SSL Order ' + str(data.json()['id']) + ' (More Info)',
                               body='Common Name: ' + str(data.json()['certificate']['common_name']) + '\n' \
                                    'Valid From: ' + str(data.json()['certificate']['valid_from']) + '\n' \
                                    'Valid Until: ' + str(data.json()['certificate']['valid_till']) + '\n' \
                                    'Status: ' + str(data.json()['status']),
                               link='https://www.digicert.com/secure/orders/#' + str(data.json()['id']),
                               color='#439FE0', in_reply_to=msg)
            except:
                return '***Error*** Unable to find what you requested'
