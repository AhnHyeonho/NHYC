
/* global kakao */
import { withStyles, makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

import LinkIcon from '@material-ui/icons/Link';
import RoomIcon from '@material-ui/icons/Room';

import React, { useState, useEffect } from 'react';
import axios from 'axios';

import './RecommandTable.css'
import { create } from 'domain';




// Custom table row 
const StyledTableRow = withStyles((theme) => ({
    root: {
        '&:nth-of-type(odd)': {
            backgroundColor: theme.palette.action.hover,
        },
    },
}))(TableRow);





// Custom table cell
const StyledTableCell = withStyles((theme) => ({

    head: {
        backgroundColor: theme.palette.common.white,
        color: theme.palette.common.black,
        padding: "5px 2px 8px 2px"

    },

    body: {
        fontSize: 13,
        padding: "7px 5px 7px 5px",
    },
}))(TableCell);







function createData(index, address, latitude, longitude, index2, address2, latitude2, longitude2) {

    // 네이버 부동산 이동 링크 (각 동의 중심 좌표로 이동)
    let url = "https://new.land.naver.com/complexes?ms=" + latitude + "," + longitude + ",16&a=APT:ABYG:JGC&e=RETAIL";

    let url2 = "https://new.land.naver.com/complexes?ms=" + latitude2 + "," + longitude2 + ",16&a=APT:ABYG:JGC&e=RETAIL";


    return { index, address, latitude, longitude, url, index2, address2, latitude2, longitude2, url2 };
}



// *** 테이블 헤더 ***

const columns = [

    { id: 'rank1', align: 'center', label: '순위', minWidth: 45 },
    { id: 'name1', align: 'center', label: '지역명', minWidth: 120 },
    { id: 'map-btn1', align: 'center', label: '', minWidth: 5 },
    { id: 'naver-btn1', align: 'center', label: '', minWidth: 5 },

    { id: 'rank2', align: 'center', label: '순위', minWidth: 45 },
    { id: 'name2', align: 'center', label: '지역명', minWidth: 120 },
    { id: 'map-btn2', align: 'center', label: '', minWidth: 5 },
    { id: 'naver-btn2', align: 'center', label: '', minWidth: 5 },

];

// *************

const useStyles = makeStyles({
    table: {
        minWidth: 200
    },
});

const rows =[
    createData(1, "서울시 강북구 5동", )

]
// let rows = []

export default function RecommandTable(props) {

    // API Test ======
    // 테이블 row에 들어갈 
    const [address, setAddress] = useState(null);
    const [latitude, setLatitude] = useState(null);
    const [longtitude, setLongtitude] = useState(null);

    const [users, setUsers] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    // ===============

    const classes = useStyles();


    function changeMap(lat, lon){
       
        props.changeMap(lat, lon);
    }
    

    // API Test ===============
    useEffect(() => {

        const fetchUsers = async () => {
            try {

                // 요청이 시작 할 때에는 error 와 users 를 초기화하고
                setError(null);
                setUsers(null);

                // loading 상태를 true 로 바꿈
                setLoading(true);
                const response = await axios.get(

                    'http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/dummyData/'
                );

                const resData = response.data[""]


                // 추후에 model로 리팩토링
                const resRank = resData.map(data => data.rank);
                const resAddr = resData.map(data => data.address);
                const resLat = resData.map(data => data.latitude);
                const resLon = resData.map(data => data.longitude);


                resData.forEach(function (element, i, array) {
                    if (i < 5) {
                        rows[i] = createData(resRank[i], resAddr[i], resLat[i], resLon[i], resRank[i + 5], resAddr[i + 5], resLat[i + 5], resLon[i + 5]);
                    }

                });

                console.log(rows);


            } catch (e) {
                setError(e);
                console.log(e);
            }

            setLoading(false);
        };


        fetchUsers();
    }, []);




    if (loading) return <div>로딩중..</div>;
    if (error) return <div>에러가 발생했습니다</div>;
    // if (!users) return null;



    console.log(rows);

    return (

        <TableContainer component={Paper}>
            <Table className={classes.table} size="small" aria-label="customized table">

                {/* 테이블 헤더 */}
                <TableHead>
                    <StyledTableRow>

                        {columns.map((column) => (
                            <StyledTableCell
                                key={column.id}
                                align={column.align}
                                style={{ minWidth: column.minWidth }}
                            >
                                {column.label}
                            </StyledTableCell>
                        ))}

                    </StyledTableRow>
                </TableHead>

                {/* 테이블 바디 */}
                <TableBody>

                    {rows.map((row, index) => (
                        <StyledTableRow key={index} >


                            <StyledTableCell align="center" > {row.index} </StyledTableCell>
                            <StyledTableCell align="center"> {row.address} </StyledTableCell>
                            <StyledTableCell align="center" ><button className="map-btn" onClick={()=>changeMap(row.latitude,row.longitude)}><RoomIcon style={{ fill: "#1976d2" }} /></button></StyledTableCell>
                            <StyledTableCell align="center" ><a href={row.url}><LinkIcon style={{ fill: "#1976d2" }} /></a></StyledTableCell>


                            <StyledTableCell align="center">{row.index2}</StyledTableCell>
                            <StyledTableCell align="center">{row.address2}</StyledTableCell>
                            <StyledTableCell align="center" ><button className="map-btn"  onClick={()=>changeMap(row.latitude2,row.longitude2)}><RoomIcon style={{ fill: "#1976d2" }} /></button></StyledTableCell>
                            <StyledTableCell align="center" ><a href={row.url}><LinkIcon style={{ fill: "#1976d2" }} /></a></StyledTableCell>


                        </StyledTableRow>
                    ))}

                </TableBody>
            </Table>
        </TableContainer>
    );
}
