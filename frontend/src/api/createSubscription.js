const GH_ALERTS_API_ENDPOINT = process.env.REACT_APP_GH_ALERTS_API;

const createSubscription = async (values) => {
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(values),
  };

  const response = await fetch(
    `${GH_ALERTS_API_ENDPOINT}/subscriptions`,
    options
  );
  const json = await response.json();

  return { status: response.status, ...json };
};

export default createSubscription;
