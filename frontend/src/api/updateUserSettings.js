const GH_ALERTS_API_ENDPOINT = process.env.REACT_APP_GH_ALERTS_API;

const updateUserSettings = async (username) => {
  const options = {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    // TODO: add user info in body
  };
  const response = await fetch(
    // `${GH_ALERTS_API_ENDPOINT}/users/${username}`,
    `${GH_ALERTS_API_ENDPOINT}`
  );
  console.log(response.text);
  const json = await response.json();

  return { status: response.status, ...json };
};

export default updateUserSettings;
