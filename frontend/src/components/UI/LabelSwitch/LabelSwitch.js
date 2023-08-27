import * as React from 'react';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';

const LabelSwitch = (props) => {
  return (
    <FormGroup>
      <FormControlLabel control={<Switch />} label={props.label} />
    </FormGroup>
  );
};

export default LabelSwitch;
