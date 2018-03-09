from slacker import Slacker


def log(slack_channel, slack_text, property_name, property_id, dataset_name,
        dataset_type, dataset_id, dataset_schema, dataset_ui_link):
    print '[-] sending slack notfication...'
    # Set Slack Parameters
    key = 'xoxb-17072631142-Xz5PVLnzfUEL16KznUJPZWgT'  # @ep-bot
    slack = Slacker(key)

    print '[?] Sending message to Slack...'
    attachments = [
        {"color": "good",
         "title": "Google Analytics Details:",
            "text": "Property Name: %s \n Property ID: %s \n Data Set Name: %s \n Data Set Type: %s \n Data Set ID: %s \n Data Set Schema: %s \n Data Imports Link: %s" %
         (property_name, property_id, dataset_name,
          dataset_type, dataset_id, dataset_schema, dataset_ui_link)
         }
    ]

    slack.chat.post_message(
        channel=slack_channel,
        text=slack_text,
        unfurl_links='false',
        as_user='true',
        attachments=attachments)

    print '[x] slack notification sent successfully.'

if __name__ == '__main__':
    log()
