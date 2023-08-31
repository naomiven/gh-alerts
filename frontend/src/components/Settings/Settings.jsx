import { useState } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import LabelSwitch from '../UI/LabelSwitch/LabelSwitch';
import DestinationInput from '../UI/DestinationInput/DestinationInput';
import updateUserSettings from '../../api/updateUserSettings';
import './Settings.css';

const Settings = (props) => {
  // TODO: use get for initial state
  const [values, setValues] = useState({
    username: 'naomiven', // TODO: use username in storage
    scheduledAlerts: false,
    livePRAlerts: false,
    email: '',
    phoneNumber: '',
    trackingRepos: '*',
  });
  // Curried function - handle change for any input
  const onChange = (input) => (event) => {
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    setValues(prevValues => ({...prevValues, [input]: value}));
  }

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
            <LabelSwitch
              label='Receive scheduled notifications'
              value={values.scheduledAlerts}
              onChange={onChange('scheduledAlerts')}
            ></LabelSwitch>
            <LabelSwitch
              label='Receive real-time Pull Requests'
              value={values.livePRAlerts}
              onChange={onChange('livePRAlerts')}
            ></LabelSwitch>
            <DestinationInput
              label='Email'
              buttonLabel='Subscribe'
              value={values.email}
              onChange={onChange('email')}
            ></DestinationInput>
            <DestinationInput
              label='Phone Number'
              buttonLabel='Subscribe'
              value={values.phoneNumber}
              onChange={onChange('phoneNumber')}
            ></DestinationInput>
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
