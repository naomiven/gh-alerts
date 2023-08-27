import LabelSwitch from '../UI/LabelSwitch/LabelSwitch';

const Settings = (props) => {
  return (
    <>
      <p>Settings</p>
      <LabelSwitch label='Receive scheduled notifications'></LabelSwitch>
      <LabelSwitch label='Receive real-time Pull Requests'></LabelSwitch>
    </>
  );
};

export default Settings;
