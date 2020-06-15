import React, { useState } from 'react';
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



export default function UserInfoSection(props) {

  const classes = useStyles();

  const ageGroupLabel = ['1~9', '10~14', '15~19', '20~29', '30~39', '40~49', '50~59', '60~69', '70~79', '80~89', '90~'];

  const [userInfo, setUserInfo] = useState({
    id: '',
    email: '',
    password: '',
    rePassword: '',
    name: '',
    sex: '',
    ageGroup: '',
    monthlyRent: '',
    deposit: '',
  });



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
            label="아이디 (id)"
            fullWidth
            autoComplete="id"
            onChange={e=> { props.handleUserInfo("id", e.target.value)}}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            required
            id="email"
            name="email"
            label="이메일 (e-mail)"
            fullWidth
            autoComplete="email"
            onChange={e=> { props.handleUserInfo("email", e.target.value)}}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            required
            id="password"
            name="password"
            label="비밀번호 (password)"
            fullWidth
            autoComplete="password"
            type="password"
            onChange={e=> { props.handleUserInfo("password", e.target.value)}}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            required
            id="rePassword"
            name="rePassword"
            label="비밀번호 확인 (password confirm)"
            fullWidth
            autoComplete="password comfirm"
            type="password"
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            required
            id="name"
            name="name"
            label="이름 (name)"
            fullWidth
            autoComplete="name"
            onChange={e=> { props.handleUserInfo("name", e.target.value)}}
          />
        </Grid>

        <Grid item xs={12} sm={3}>
          {/* 성별 */}
          <FormControl className={classes.formControl}>
            <InputLabel htmlFor="grouped-native-select">성별</InputLabel>
            <Select native defaultValue="" id="grouped-native-select" onChange={e=> { props.handleUserInfo("sex", e.target.value)}}>

              <option aria-label="None" value="" />
              <option value={"f"} id="f">여자 (female)</option>
              <option value={"m"} id="m">남자 (male)</option>

            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} sm={3}>
          {/* 나이 */}

          <FormControl className={classes.formControl}>
            <InputLabel htmlFor="grouped-native-select">연령대</InputLabel>
            <Select native defaultValue="" id="grouped-native-select" onChange={e=> { props.handleUserInfo("ageGroup",ageGroupLabel[e.target.value] ) } }>

              <option aria-label="None" value="" />
              {
                ageGroupLabel.map((label, i) => (
                <option key={i} value={i}>{label}</option>
                ))
              }

            </Select>
          </FormControl>

        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            id="monthly"
            name="monthly"
            label="희망 월세 가격 (만원)"
            fullWidth
            autoComplete="monthly"
            onChange={e=> { props.handleUserInfo("monthly", e.target.value)}}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            id="deposit"
            name="deposit"
            label="희망 보증금 가격 (만원)"
            fullWidth
            autoComplete="Deposit"
            onChange={e=> { props.handleUserInfo("deposit", e.target.value)}}
          />
        </Grid>
      </Grid>
    </React.Fragment>
  );
}