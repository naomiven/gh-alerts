import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '../BasicButton/BasicButton';

const DestinationInput = (props) => {
  return (
    <>
      <TextField id='outlined-basic' variant='outlined' label={props.label} value={props.value}/>
      <Button label={props.buttonLabel}></Button>
    </>
  );
};

export default DestinationInput;
