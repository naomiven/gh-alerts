import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';

const LabelSwitch = (props) => {
  return (
    <FormGroup>
      <FormControlLabel control={<Switch checked={props.value} onChange={props.onChange}/>} label={props.label}/>
    </FormGroup>
  );
};

export default LabelSwitch;
