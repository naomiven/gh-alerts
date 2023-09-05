import TextField from '@mui/material/TextField';
import Button from '../UI/BasicButton/BasicButton';
import './SubscriptionInput.css';

const SubscriptionInput = (props) => {
  return (
    <div className='stack'>
      {props.label}
      <div className='subscriptionInput'>
        <TextField
          id='outlined-basic'
          variant='outlined'
          label={props.label}
          value={props.value}
          onChange={props.onChange}
        />
        <Button label={props.buttonLabel}></Button>
      </div>
    </div>
  );
};

export default SubscriptionInput;
