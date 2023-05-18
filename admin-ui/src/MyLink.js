import { Link } from 'react-router-dom';

const MyLink = ({ children, ...props }) => (
    <Link
        style={{ textDecoration: 'none', color: 'inherit' }}
        {...props}
    >
        {children}
    </Link>
);

export default MyLink;
