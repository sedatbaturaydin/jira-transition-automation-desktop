# jira_api.py
import os
from dotenv import load_dotenv
from jira import JIRA

load_dotenv()

jira_url = os.getenv('JIRA_URL')
jira_username = os.getenv('JIRA_USERNAME')
jira_token = os.getenv('JIRA_API_TOKEN')

# Jira'ya bağlan
try:
    jira = JIRA(jira_url, basic_auth=(jira_username, jira_token))
except Exception as e:
    print(f"Jira bağlantısı başarısız: {e}")
    exit()

# Talepleri çek
def get_my_open_issues():
    jql_query = jql_query = f'assignee = currentUser() AND (status = "Açık" OR status = "Çalışılıyor" OR status = "Talep Sahibinden Bilgi Bekleniyor") OR  assignee IS NULL AND status = "Açık" ORDER BY created DESC'
    return jira.search_issues(jql_query, maxResults=50)

# Statü değiştir
def transition_issue(issue_key, transition_id):
    jira.transition_issue(issue_key, transition_id)

# Yorum ekle
def add_comment(issue_key, comment):
    jira.add_comment(issue_key, comment)
