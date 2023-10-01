import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import './SubscriptionInput.css';

const SubscriptionInput = (props) => {
  return (
    <div className='stack'>
      {props.label}
      <div className='subscriptionInput'>
        <TextField
          className='textfield'
          id='outlined-basic'
          variant='outlined'
          label={props.label}
          value={props.value}
          onChange={props.onChange}
        />
        <Button variant='contained' onClick={props.onSubscribe}>
          {props.buttonLabel}
        </Button>
      </div>
    </div>
  );
};

export default SubscriptionInput;
