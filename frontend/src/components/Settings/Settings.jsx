import Box from '@mui/material/Box';
import Button from '../UI/BasicButton/BasicButton';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import LabelSwitch from '../UI/LabelSwitch/LabelSwitch';
import DestinationInput from '../UI/DestinationInput/DestinationInput';

const Settings = (props) => {
  return (
    <>
      <Container maxWidth='sm'>
        <Typography variant='h4' style={{ marginBottom: '20px' }}>
          Settings
        </Typography>
        <Box sx={{ bgcolor: '#cfe8fc', height: '100vh' }}>
          <LabelSwitch label='Receive scheduled notifications'></LabelSwitch>
          <LabelSwitch label='Receive real-time Pull Requests'></LabelSwitch>
          <DestinationInput
            label='Email'
            buttonLabel='Subscribe'
          ></DestinationInput>
          <DestinationInput
            label='Phone Number'
            buttonLabel='Subscribe'
          ></DestinationInput>
          <Button label='Save'></Button>
        </Box>
      </Container>
    </>
  );
};

export default Settings;
