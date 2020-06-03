import React from 'react';
import { withStyles, makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

const StyledTableCell = withStyles((theme) => ({
    head: {
      backgroundColor: theme.palette.common.black,
      color: theme.palette.common.white,
    },
    body: {
      fontSize: 14,
    },
  }))(TableCell);
  const StyledTableRow = withStyles((theme) => ({
    root: {
      '&:nth-of-type(odd)': {
        backgroundColor: theme.palette.action.hover,
      },
    },
  }))(TableRow);

function createData(rank1, name1, rank2, name2) {
    return { rank1, name1, rank2, name2 };
}

// 
const rows = [
    createData(1, '서울특별시 성북구 성북동', 2, '서울특별시 노원구 방학동'),
    createData(1, '서울특별시 성북구 성북동', 2, '서울특별시 노원구 방학동'),
    createData(1, '서울특별시 성북구 성북동', 2, '서울특별시 노원구 방학동'),
    createData(1, '서울특별시 성북구 성북동', 2, '서울특별시 노원구 방학동'),
];

// Header colums
const columns = [
    { id: 'rank1', align: 'left', label: '순위', minWidth: 40 },
    { id: 'name1', align: 'left', label: '지역명', minWidth: 80 },
    { id: 'rank2', align: 'left', label: '순위', minWidth: 40 },
    { id: 'name2', align: 'left', label: '지역명', minWidth: 80 }
];

const useStyles = makeStyles({
    table: {
        minWidth: 200
    },
});



export default function RecommandTable() {

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

                    {rows.map((row) => (
                        <StyledTableRow 
                            key={row.name} 
                            StyledTableRow={StyledTableRow} 
                            StyledTableCell={StyledTableCell}
                        >
                            <StyledTableCell align="right">{row.name1}</StyledTableCell>
                            <StyledTableCell align="right">{row.rank1}</StyledTableCell>
                            <StyledTableCell align="right">{row.rank2}</StyledTableCell>
                            <StyledTableCell align="right">{row.name2}</StyledTableCell>

                        </StyledTableRow>
                    ))}
                    
                </TableBody>


            </Table>
        </TableContainer>
    );
}
