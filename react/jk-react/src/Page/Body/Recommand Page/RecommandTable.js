
import { withStyles, makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import LinkIcon from '@material-ui/icons/Link';

import React, { useState, useEffect } from 'react';
import axios from 'axios';

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
        padding: "6px 10px 6px 10px"
    },

    body: {
        fontSize: 14,
        padding: "6px 10px 6px 10px",
    },
}))(TableCell);



// response 값 Object화 
// function createData(rank1, name1, rank2, name2) {

//     // Object return 
//     return { rank1, name1, rank2, name2 };
// }

function createData(index, address, latitude, longtitude){

    let url = "https://new.land.naver.com/complexes?ms="+ latitude + "," + longtitude + ",16&a=APT:ABYG:JGC&e=RETAIL";

    return { index, address, url };
}



const rows = [
    createData(1, '서울특별시 성북구 성북동', 37.5969, 126.9922),
    createData(2, '서울특별시 성북구 성북동', 37.5969, 126.9922),
    createData(3, '서울특별시 성북구 성북동', 37.5969, 126.9922),
    createData(4, '서울특별시 성북구 성북동', 37.5969, 126.9922),
    createData(5, '서울특별시 성북구 성북동', 37.5969, 126.9922),
    createData(6, '서울특별시 성북구 성북동', 37.5969, 126.9922),
    createData(7, '서울특별시 성북구 성북동', 37.5969, 126.9922),
    createData(8, '서울특별시 성북구 성북동', 37.5969, 126.9922),
    createData(9, '서울특별시 성북구 성북동', 37.5969, 126.9922),
    createData(10, '서울특별시 성북구 성북동', 37.5969, 126.9922),
];

// Header colums
const columns = [
    { id: 'rank1', align: 'left', label: '순위', minWidth: 20 },
    { id: 'name1', align: 'left', label: '지역명', minWidth: 100 },
    { id: 'btn1', align: 'left', label: '', minWidth: 10 },

    { id: 'rank2', align: 'left', label: '순위', minWidth: 20 },
    { id: 'name2', align: 'left', label: '지역명', minWidth: 100 },
    { id: 'btn2', align: 'left', label: '', minWidth: 10 },

];

const useStyles = makeStyles({
    table: {
        minWidth: 200
    },
});



export default function RecommandTable() {

    // API Test ======
    const [users, setUsers] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    // ===============

    const classes = useStyles();

    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(10);

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(+event.target.value);
        setPage(0);
    };


    const handleClick=(event, url)=> {
        console.log(url);
        //  window.location = url;
    }

    

    // useEffect(
    //     () => {
    //         fetch('https://jsonplaceholder.typicode.com/posts')
    //             .then(res => {
    //                 console.log(res.json()[0]['userId']);
    //             })
    //         // .then(data => title = data["0"]["title"])
    //         // .then(data => console.log(data))
    //         // .then(data => options["title"]["text"] = title)
    //         // .then()
    //     },
    // );


    // API Test ===============
    useEffect(() => {

        const fetchUsers = async () => {
            try {

                // 요청이 시작 할 때에는 error 와 users 를 초기화하고
                setError(null);
                setUsers(null);

                // loading 상태를 true 로 바꿉니다.
                setLoading(true);
                const response = await axios.get(
                    'https://jsonplaceholder.typicode.com/users'
                );

                setUsers(response.data); // 데이터는 response.data 안에 들어있습니다.

            } catch (e) {
                setError(e);
            }

            setLoading(false);
        };


        fetchUsers();
    }, []);

    // ========================

    


    
    if (loading) return <div>로딩중..</div>;
    if (error) return <div>에러가 발생했습니다</div>;
    if (!users) return null;

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

                    {rows.map((user, index) => (

                        <StyledTableRow key={index} >
                            
                            <StyledTableCell align="left">{user.index}</StyledTableCell>
                            <StyledTableCell align="left">{user.address}</StyledTableCell>
                                <StyledTableCell align="left" ><a href={user.url}><LinkIcon style={{ fill: "#1976d2" }} /></a></StyledTableCell>
                            

                            <StyledTableCell align="left">{user.index}</StyledTableCell>
                            <StyledTableCell align="left">{user.address}</StyledTableCell>
                            <StyledTableCell align="left"><LinkIcon style={{ fill: "#1976d2" }} /></StyledTableCell>


                        </StyledTableRow>
                    ))}

                </TableBody>
            </Table>
        </TableContainer>
    );
}
