import TextField from '@mui/material/TextField';
import Button from '../BasicButton/BasicButton';
import './DestinationInput.css';

const DestinationInput = (props) => {
  return (
    <div className='destinationInput'>
      <TextField
        id='outlined-basic'
        variant='outlined'
        label={props.label}
        value={props.value}
        onChange={props.onChange}
      />
      <Button label={props.buttonLabel}></Button>
    </div>
  );
};

export default DestinationInput;
