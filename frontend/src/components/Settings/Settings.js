import LabelSwitch from '../UI/LabelSwitch/LabelSwitch';
import DestinationInput from '../UI/DestinationInput/DestinationInput';

const Settings = (props) => {
  return (
    <>
      <p>Settings</p>
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
    </>
  );
};

export default Settings;
