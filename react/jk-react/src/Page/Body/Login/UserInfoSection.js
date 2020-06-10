import React from 'react';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';

// About Drop Box
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import ListSubheader from '@material-ui/core/ListSubheader';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';


const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
}));



export default function UserInfoSection() {

  const classes = useStyles();

  return (
    <React.Fragment>

      <Typography variant="h6" gutterBottom>
        User Info
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6}>
          <TextField
            required
            id="id"
            name="id"
            label="Id"
            fullWidth
            autoComplete="id"
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            required
            id="email"
            name="email"
            label="E-Mail"
            fullWidth
            autoComplete="email"
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            required
            id="password"
            name="password"
            label="Password"
            fullWidth
            autoComplete="password"
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            required
            id="password"
            name="password"
            label="Password Confirm"
            fullWidth
            autoComplete="password comfirm"
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            required
            id="name"
            name="name"
            label="Name"
            fullWidth
            autoComplete="name"
          />
        </Grid>
        
        <Grid item xs={12} sm={3}>
          {/* 성별 */}
          <FormControl className={classes.formControl}>
            <InputLabel htmlFor="grouped-native-select">Sex</InputLabel>
            <Select native defaultValue="" id="grouped-native-select">
              <option aria-label="None" value="" />
              <optgroup label="Category 1">
                <option value={1}>Option 1</option>
                <option value={2}>Option 2</option>
              </optgroup>
              <optgroup label="Category 2">
                <option value={3}>Option 3</option>
                <option value={4}>Option 4</option>
              </optgroup>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} sm={3}>
          {/* 나이 */}
          <FormControl className={classes.formControl}>
            <InputLabel htmlFor="grouped-select">Age Group</InputLabel>
            <Select defaultValue="" id="grouped-select">
              <MenuItem value="">
                <em>None</em>
              </MenuItem>
              <ListSubheader>Category 1</ListSubheader>
              <MenuItem value={1}>Option 1</MenuItem>
              <MenuItem value={2}>Option 2</MenuItem>
              <ListSubheader>Category 2</ListSubheader>
              <MenuItem value={3}>Option 3</MenuItem>
              <MenuItem value={4}>Option 4</MenuItem>
            </Select>
          </FormControl>

        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            id="monthly"
            name="monthly"
            label="Monthly Rent"
            fullWidth
            autoComplete="monthly"
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            id="deposit"
            name="deposit"
            label="Deposit"
            fullWidth
            autoComplete="Deposit"
          />
        </Grid>
        <Grid item xs={12}>
          <FormControlLabel
            control={<Checkbox color="secondary" name="saveAddress" value="yes" />}
            label="Use this address for payment details"
          />
        </Grid>
      </Grid>
    </React.Fragment>
  );
}