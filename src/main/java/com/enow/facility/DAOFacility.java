package com.enow.facility;

import com.enow.daos.redisDAO.INodeDAO;
import com.enow.daos.redisDAO.NodeDAO;

/**
 * Created by writtic on 2016. 9. 12..
 */

public class DAOFacility implements IDAOFacility {
    private static IDAOFacility _instance;

    /**
     * Constructor
     */
    private DAOFacility(){

    }

    /**
     * Gets the instance of the DAOFacility
     * @return
     */
    public static IDAOFacility getInstance(){
        if(_instance == null)
            _instance = new DAOFacility();

        return _instance;
    }

    /**
     * Creates a new NodeDAO
     *
     * @return NodeDAO that implements INodeDAO
     */
    @Override
    public INodeDAO createPeerDAO() {
        return new NodeDAO();
    }

}
