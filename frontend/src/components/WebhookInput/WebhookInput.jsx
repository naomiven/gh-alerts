import TextField from '@mui/material/TextField';
import './WebhookInput.css';

const WebhookInput = (props) => {
  return (
    <div className='stack'>
      {props.label}
      <TextField
        className='textfield'
        id='outlined-basic'
        variant='outlined'
        value={props.value}
        onChange={props.onChange}
      />
    </div>
  );
};

export default WebhookInput;
