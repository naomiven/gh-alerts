import { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import LabelSwitch from '../../components/UI/LabelSwitch/LabelSwitch';
import Toast from '../../components/UI/Toast/Toast';
import SubscriptionInput from '../../components/SubscriptionInput/SubscriptionInput';
import WebhookInput from '../../components/WebhookInput/WebhookInput';
import createSubscription from '../../api/createSubscription';
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
    msTeamsWebhookURL: '',
    slackWebhookURL: '',
    trackingRepos: '*',
  });

  const [toast, setToast] = useState({
    message: null,
    severity: null,
    open: false,
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
        msTeamsWebhookURL: response.msTeamsWebhookURL,
        slackWebhookURL: response.slackWebhookURL,
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

  // Need extra () because we don't want this to execute when calling subscribeHandler(...).
  // We want it to return a function.
  const subscribeHandler = (input) => () => {
    const asyncCreateSubscription = async () => {
      const response = await createSubscription({ [input]: values[input] });

      if (response.status === 200) {
        setToast(() => ({
          message:
            input === 'email'
              ? 'Email subscribed successfully.' +
                'Please check your email to confirm your subscription.'
              : input === 'phoneNumber'
              ? 'Phone number subscribed successfully!'
              : null,
          severity: 'success',
          open: true,
        }));
      } else {
        setToast(() => ({
          message: 'Subscribe failed!',
          severity: 'error',
          open: true,
        }));
      }
    };
    asyncCreateSubscription();
  };

  const submitHandler = (event) => {
    event.preventDefault();

    const asyncUpdateUserSettings = async () => {
      const response = await updateUserSettings(values);

      if (response.status === 200) {
        setToast(() => ({
          message: 'Settings saved successfully!',
          severity: 'success',
          open: true,
        }));
      } else {
        setToast(() => ({
          message: 'Save failed!',
          severity: 'error',
          open: true,
        }));
      }
    };
    asyncUpdateUserSettings();
  };

  const closeToastHandler = (event) => {
    setToast(() => ({ message: null, severity: null, open: false }));
  };

  return (
    <>
      <Container maxWidth='sm'>
        <Toast
          message={toast.message}
          severity={toast.severity}
          open={toast.open}
          onClose={closeToastHandler}
        />
        <Typography variant='h4'>
          <div className='title-settings'>Settings</div>
        </Typography>
        <Box
          onSubmit={submitHandler}
          // sx={{ bgcolor: '#cfe8fc', height: '200vh' }}
        >
          <form onSubmit={submitHandler} className='form'>
            <h2>Subscribe to Notifications</h2>
            <LabelSwitch
              label='Receive scheduled notifications'
              value={values.scheduledAlerts}
              onChange={changeHandler('scheduledAlerts')}
            />
            <LabelSwitch
              label='Receive real-time Pull Requests'
              value={values.livePRAlerts}
              onChange={changeHandler('livePRAlerts')}
            />
            <SubscriptionInput
              label='Email'
              buttonLabel='Subscribe'
              value={values.email}
              onChange={changeHandler('email')}
              onSubscribe={subscribeHandler('email')}
            />
            <SubscriptionInput
              label='Phone Number'
              buttonLabel='Subscribe'
              value={values.phoneNumber}
              onChange={changeHandler('phoneNumber')}
              onSubscribe={subscribeHandler('phoneNumber')}
            />
            <h2>Register Webhooks</h2>
            <WebhookInput
              label='MS Teams Webhook URL'
              value={values.msTeamsWebhookURL}
              onChange={changeHandler('msTeamsWebhookURL')}
            />
            <WebhookInput
              label='Slack Webhook URL'
              value={values.slackWebhookURL}
              onChange={changeHandler('slackWebhookURL')}
            />
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
