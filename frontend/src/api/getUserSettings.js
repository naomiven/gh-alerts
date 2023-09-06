const GH_ALERTS_API_ENDPOINT = process.env.REACT_APP_GH_ALERTS_API;

const getUserSettings = async (username) => {
  const response = await fetch(`${GH_ALERTS_API_ENDPOINT}/users/${username}`);
  const json = await response.json();
  console.log(json);

  const subs = json.sns_subscriptions;
  const webhooks = json.webhooks;

  let email = '',
    phoneNumber = '',
    msTeamsWebhookURL = '',
    slackWebhookURL = '';

  if (subs) {
    email = subs.find((item) => item.protocol === 'email')
      ? subs.find((item) => item.protocol === 'email').endpoint
      : '';
    phoneNumber = subs.find((item) => item.protocol === 'phone_number')
      ? subs.find((item) => item.protocol === 'phone_number').endpoint
      : '';
  }

  if (webhooks) {
    msTeamsWebhookURL = webhooks.find((item) => item.name === 'ms_teams')
    ? webhooks.find((item) => item.name === 'ms_teams').url
    : '';
    slackWebhookURL = webhooks.find((item) => item.name === 'slack')
    ? webhooks.find((item) => item.name === 'slack').url
    : '';
  }

  const formatted = {
    scheduledAlerts: json.scheduled_alerts,
    livePRAlerts: json.live_pr_alerts,
    email: email,
    phoneNumber: phoneNumber,
    msTeamsWebhookURL: msTeamsWebhookURL,
    slackWebhookURL: slackWebhookURL,
    trackingRepos: json.tracking_repos,
  };

  return { status: response.status, ...formatted };
};

export default getUserSettings;
