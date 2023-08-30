const GH_ALERTS_API_ENDPOINT = process.env.REACT_APP_GH_ALERTS_API;

const updateUserSettings = async (values) => {
  const options = {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(values)
  };

  const response = await fetch(
    `${GH_ALERTS_API_ENDPOINT}/users/${values.username}`, options
  );
  const json = await response.json();

  return { status: response.status, ...json };
};

export default updateUserSettings;
