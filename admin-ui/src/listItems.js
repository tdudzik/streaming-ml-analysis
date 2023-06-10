import * as React from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import DashboardIcon from '@mui/icons-material/Dashboard';
import TableChartIcon from '@mui/icons-material/TableChart';
import ModelTrainingIcon from '@mui/icons-material/ModelTraining';
import BarChartIcon from '@mui/icons-material/BarChart'; // import this for Inferences icon
import MyLink from './MyLink';

export const mainListItems = (
    <React.Fragment>
        <MyLink to="/">
            <ListItemButton>
                <ListItemIcon>
                    <DashboardIcon />
                </ListItemIcon>
                <ListItemText primary="Dashboard" />
            </ListItemButton>
        </MyLink>
        <MyLink to="/datasets">
            <ListItemButton>
                <ListItemIcon>
                    <TableChartIcon />
                </ListItemIcon>
                <ListItemText primary="Datasets" />
            </ListItemButton>
        </MyLink>
        <MyLink to="/trainings">
            <ListItemButton>
                <ListItemIcon>
                    <ModelTrainingIcon />
                </ListItemIcon>
                <ListItemText primary="Trainings" />
            </ListItemButton>
        </MyLink>
        <MyLink to="/inferences">
            <ListItemButton>
                <ListItemIcon>
                    <BarChartIcon />
                </ListItemIcon>
                <ListItemText primary="Inferences" />
            </ListItemButton>
        </MyLink>
    </React.Fragment>
);