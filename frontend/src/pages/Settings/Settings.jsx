import { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import LabelSwitch from '../../components/UI/LabelSwitch/LabelSwitch';
import SubscriptionInput from '../../components/SubscriptionInput/SubscriptionInput';
import getUserSettings from '../../api/getUserSettings';
import updateUserSettings from '../../api/updateUserSettings';
import './Settings.css';

const Settings = (props) => {
  const [values, setValues] = useState({
    username: 'naomiven', // TODO: use username in storage
    scheduledAlerts: false,
    livePRAlerts: false,
    email: '',
    phoneNumber: '',
    trackingRepos: '*',
  });

  useEffect(() => {
    const asyncGetUserSettings = async () => {
      console.log('Getting user settings...');
      const response = await getUserSettings(values.username);

      const newState = {
        scheduledAlerts: response.scheduledAlerts,
        livePRAlerts: response.livePRAlerts,
        email: response.email,
        phoneNumber: response.phoneNumber,
        trackingRepos: response.trackingRepos,
      };
      setValues((prevState) => ({ ...prevState, ...newState }));
    };
    asyncGetUserSettings();
  }, []);

  // Curried function - handle change for any input
  const changeHandler = (input) => (event) => {
    const value =
      event.target.type === 'checkbox'
        ? event.target.checked
        : event.target.value;
    setValues((prevState) => ({ ...prevState, [input]: value }));
  };

  const submitHandler = (event) => {
    event.preventDefault();
    updateUserSettings(values);
  };

  return (
    <>
      <Container maxWidth='sm'>
        <Typography variant='h4' style={{ marginBottom: '20px' }}>
          Settings
        </Typography>
        <Box
          onSubmit={submitHandler}
          sx={{ bgcolor: '#cfe8fc', height: '100vh' }}
        >
          <form onSubmit={submitHandler} className='form'>
            <h2>Subscribe to Notifications</h2>
            <LabelSwitch
              label='Receive scheduled notifications'
              value={values.scheduledAlerts}
              onChange={changeHandler('scheduledAlerts')}
            ></LabelSwitch>
            <LabelSwitch
              label='Receive real-time Pull Requests'
              value={values.livePRAlerts}
              onChange={changeHandler('livePRAlerts')}
            ></LabelSwitch>
            <SubscriptionInput
              label='Email'
              buttonLabel='Subscribe'
              value={values.email}
              onChange={changeHandler('email')}
            ></SubscriptionInput>
            <SubscriptionInput
              label='Phone Number'
              buttonLabel='Subscribe'
              value={values.phoneNumber}
              onChange={changeHandler('phoneNumber')}
            ></SubscriptionInput>
            <h2>Register Webhooks</h2>
            <Button type='submit' variant={'contained'} className='button'>
              Save
            </Button>
          </form>
        </Box>
      </Container>
    </>
  );
};

export default Settings;
