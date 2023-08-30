import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '../BasicButton/BasicButton';

const DestinationInput = (props) => {
  return (
    <Box
      component='form'
      sx={{
        '& > :not(style)': { m: 1, width: '25ch' },
      }}
      noValidate
      autoComplete='off'
    >
      <TextField id='outlined-basic' label={props.label} variant='outlined' />
      <Button label={props.buttonLabel}></Button>
    </Box>
  );
};

export default DestinationInput;
