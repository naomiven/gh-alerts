import { useState } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import LabelSwitch from '../UI/LabelSwitch/LabelSwitch';
import DestinationInput from '../UI/DestinationInput/DestinationInput';
import updateUserSettings from '../../api/updateUserSettings/updateUserSettings';
import React from 'react';

const Settings = (props) => {
  // TODO: use get for initial state
  const [values, setValues] = useState({
    scheduledAlerts: false,
    livePRAlerts: false,
    email: '',
    phoneNumber: ''
  });

  const scheduledAlertsChangeHandler = (event) => {
    setValues(prevState => ({...prevState, ['scheduledAlerts']: event.target.checked}));
  }

  const livePRAlertsChangeHandler = (event) => {
    setValues(prevState => ({...prevState, ['livePRAlerts']: event.target.checked}));
  }

  const emailChangeHandler = (event) => {
    setValues(prevState => ({...prevState, ['email']: event.target.value}));
  }

  const phoneNumberChangeHandler = (event) => {
    setValues(prevState => ({...prevState, ['phoneNumber']: event.target.value}));
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
        <Box onSubmit={submitHandler} sx={{ bgcolor: '#cfe8fc', height: '100vh' }}>
          <form onSubmit={submitHandler}>
            <LabelSwitch label='Receive scheduled notifications' value={values.scheduledAlerts} onChange={scheduledAlertsChangeHandler}></LabelSwitch>
            <LabelSwitch label='Receive real-time Pull Requests' value={values.livePRAlerts} onChange={livePRAlertsChangeHandler}></LabelSwitch>
            <DestinationInput
              label='Email'
              buttonLabel='Subscribe'
              value={values.email}
              onChange={emailChangeHandler}
            ></DestinationInput>
            <DestinationInput
              label='Phone Number'
              buttonLabel='Subscribe'
              value={values.phoneNumber}
              onChange={phoneNumberChangeHandler}
            ></DestinationInput>
            <Button type='submit' variant={'contained'}>
              Save
            </Button>
          </form>
        </Box>
      </Container>
    </>
  );
};

export default Settings;
