const GH_ALERTS_API_ENDPOINT = process.env.REACT_APP_GH_ALERTS_API;

const getUserSettings = async (username) => {
  const response = await fetch(`${GH_ALERTS_API_ENDPOINT}/users/${username}`);
  const json = await response.json();

  return { status: response.status, ...json };
};

export default getUserSettings;
