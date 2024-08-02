
# =============================================================================
# Loading Functions
# =============================================================================

#==============================================================================


def readGrid ( gridFile ):
    """
    Reads ADCIRC grid file
    
    Args:
        gridFile (str): full path to fort.14 file
    Returns:
        grid (dict): field names according to ADCIRC internal variables:
    http://adcirc.org/home/documentation/users-manual-v50/
    input-file-descriptions/adcirc-grid-and-boundary-information-file-fort-14/
    """
    print ('[info]: Reading the grid from ' + gridFile)
    if not os.path.exists (gridFile):
        print ('[error]: File ' + gridFile + ' does not exist.')
        return
        
    f  = open(gridFile)
    
    myDesc     = f.readline().rstrip()
    myNE, myNP = map(int, f.readline().split())    
    print ('[info]: Grid description ' + myDesc + '.')
    print ('[info]: Grid size: NE= '   + str(myNE) + ', NP=' + str(myNP) + '.')

    myPoints   = np.zeros([myNP,3], dtype=float)
    myElements = np.zeros([myNE,3], dtype=int)
    
    print ('[info]: Reading grid points...')
    for k in range(myNP):
        line            = f.readline().split()
        myPoints[k,0] = float(line[1])
        myPoints[k,1] = float(line[2])
        myPoints[k,2] = float(line[3])

    print ('[info]: Reading grid elements...')
    for k in range(myNE):
        line              = f.readline().split()
        #myElements[k,0:2] = map(int, line[2:4])
        myElements[k,0] = int (line[2])
        myElements[k,1] = int (line[3])
        myElements[k,2] = int (line[4])

    
    myNOPE   = int(f.readline().split()[0])
    myNETA   = int(f.readline().split()[0])   
    myNVDLL  = np.zeros([myNOPE], dtype=int)
    myNBDV   = np.zeros([myNOPE, myNETA], dtype=int)
    
    print ('[info]: Reading elevation-specified boundaries...' )   
    for k in range(myNOPE):
        myNVDLL [k] = int(f.readline().split()[0])
        for j in range(myNVDLL[k]):
            myNBDV[k,j] = int(f.readline().strip())

    myNBOU = int(f.readline().split()[0])
    myNVEL = int(f.readline().split()[0])   
    myNVELL      = np.zeros([myNBOU], dtype=int)
    myIBTYPE     = np.zeros([myNBOU], dtype=int)
    myNBVV       = np.zeros([myNBOU, myNVEL], dtype=int)
    myBARLANHT   = np.zeros([myNBOU, myNVEL], dtype=float)
    myBARLANCFSP = np.zeros([myNBOU, myNVEL], dtype=float)
    myIBCONN     = np.zeros([myNBOU, myNVEL], dtype=int)
    myBARINHT    = np.zeros([myNBOU, myNVEL], dtype=float)
    myBARINCFSB  = np.zeros([myNBOU, myNVEL], dtype=float)
    myBARINCFSP  = np.zeros([myNBOU, myNVEL], dtype=float)
    myPIPEHT     = np.zeros([myNBOU, myNVEL], dtype=float)
    myPIPECOEF   = np.zeros([myNBOU, myNVEL], dtype=float)
    myPIPEDIAM   = np.zeros([myNBOU, myNVEL], dtype=float)
    
    print ('[info]: Reading normal flow-specified boundaries...')    
    for k in range(myNBOU):
        line = f.readline().split()
        myNVELL[k]  = int(line[0])
        myIBTYPE[k] = int(line[1])
        
        for j in range(myNVELL[k]):
            line = f.readline().rstrip().split()            
            if myIBTYPE[k] in   [0,1,2,10,11,12,20,21,22,30]:
                myNBVV      [k,j] = int(line[0])
            elif myIBTYPE[k] in [3,13,23]:
                myNBVV      [k,j] = int  (line[0])
                myBARLANHT  [k,j] = float(line[1])
                myBARLANCFSP[k,j] = float(line[2])
            elif myIBTYPE[k] in [4,24]:
                myNBVV      [k,j] = int  (line[0])
                myIBCONN    [k,j] = int  (line[1])
                myBARINHT   [k,j] = float(line[2])
                myBARINCFSB [k,j] = float(line[3])
                myBARINCFSP [k,j] = float(line[4])
            elif myIBTYPE[k] in [5,25]:
                myNBVV      [k,j] = int  (line[0])
                myIBCONN    [k,j] = int  (line[1])
                myBARINHT   [k,j] = float(line[2])
                myBARINCFSB [k,j] = float(line[3])
                myBARINCFSP [k,j] = float(line[4])
                myPIPEHT    [k,j] = float(line[5])
                myPIPECOEF  [k,j] = float(line[6])
                myPIPEDIAM  [k,j] = float(line[7])

    f.close()
        
    return {'GridDescription'               : myDesc, 
            'NE'                            : myNE, 
            'NP'                            : myNP, 
            'lon'                           : np.squeeze(myPoints[:,0]),
            'lat'                           : np.squeeze(myPoints[:,1]), 
            'depth'                         : np.squeeze(myPoints[:,2]), 
            'Elements'                      : np.squeeze(myElements),
            'NETA'                          : myNETA, 
            'NOPE'                          : myNOPE,
            'ElevationBoundaries'           : np.squeeze(myNBDV), 
            'NormalFlowBoundaries'          : np.squeeze(myNBVV),
            'ExternalBarrierHeights'        : np.squeeze(myBARLANHT),
            'ExternalBarrierCFSPs'          : np.squeeze(myBARLANCFSP),
            'BackFaceNodeNormalFlow'        : np.squeeze(myIBCONN),
            'InternalBarrierHeights'        : np.squeeze(myBARINHT),
            'InternallBarrierCFSPs'         : np.squeeze(myBARINCFSP),
            'InternallBarrierCFSBs'         : np.squeeze(myBARINCFSB),            
            'CrossBarrierPipeHeights'       : np.squeeze(myPIPEHT),
            'BulkPipeFrictionFactors'       : np.squeeze(myPIPECOEF),            
            'CrossBarrierPipeDiameter'      : np.squeeze(myPIPEDIAM)
            }


#==============================================================================
def readSurfaceField_ascii ( asciiFile,myNP):
    """
    Reads ADCIRC 2D output file (e.g. mmaxele)
    Args:
        'asciiFile' (str): full path to ADCIRC 2D file in ASCII format
    Returns:
        value (np.array [NP, NS]), where NP - number of grid points, 
                                     and NS - number of datasets
    """
    print ('[info]: Reading ASCII file ' + asciiFile + '.')
    f  = open(asciiFile)
    
    myDesc = f.readline().strip()
    #print ('[info]: Field description [' + myDesc + '].')
    line          = f.readline().split()    
    #myNDSETSE1     = int(line[0])
    #myNP          = int(line[1])
    #print(f'[info]: Number of grid points {myNP}  {myNDSETSE1}')
    
#    myNSPOOLGE    = int(line[3])
#    myIRTYPE      = int(line[4])
#    dtdpXnspoolge = float(line[2])  

    #------locating if fewer timesteps written in fort63s
    ind_match_str = []
    chk1 = 0
    with open(asciiFile, 'r') as inF:
        
        for line in inF:  
            if f'{myNP}   ' in line:
                #print(line)    
                ind_match_str.append(chk1)
            chk1 += 1
    # # now reading that specific line to get timesteps        
    # with open(asciiFile, 'r') as inF:
    #     tss =         inF.readlines()[ind_match_str[-1]+1:ind_match_str[-1]+2]
    #     tspts = tss[0].strip(' ').split(' ')[-1][:-1]
    #     print(f'fort63 only has written only {tspts}/{myNDSETSE1} timesteps [s]')   

    tspts=len(ind_match_str)

    myNDSETSE = int(tspts)
    print(f'[info]: fort63 only has written only {tspts}/{myNDSETSE} timesteps') 

    # if myNDSETSE == myNDSETSE1:
    #     print('[info]: Complete Simulation')
    # else:
    #     print('[warning]: Incomplete Simulation')
    f.close()
    
    f  = open(asciiFile)
    line          = f.readline().split()
#    myTIME        = float(line[0])
#    myIT          = float(line[1])
    value = np.zeros([myNP,myNDSETSE], dtype=float)
    #try:
    for s in range(myNDSETSE):
        #s=0
        for n in range(myNP):
            value[n,s] = float(f.readline().split()[1]) 
        line0 = f.readline().split()# this line is must to avoid reading timestep info
    value = np.squeeze(value)
    
    fill_value = -99999.0
    value[value==fill_value]=np.nan
    # except:
    #     print('Rerun command by specifying total timesteps completed')
        
    f.close();inF.close()
    
    return value 


#==============================================================================
def readFort14 ( fort14file ):
    """
    Reads ADCIRC fort.14 file
    """
    return readGrid (fort14file)





def adcirc_nodalIdentifier(lat,lon,x2,y2):
    chosen_lat = x2  
    chosen_lon = y2
    min_distance = None
    best_index = 0
    
    for i in range(len(lat)):
        current_distance = (lat[i] - chosen_lat)**2 + (lon[i] - chosen_lon)**2
        if min_distance is None or current_distance < min_distance:
            best_index = i
            min_distance = current_distance    
    return best_index

def convert_vdatum(latitude: float, longitude: float, elevation: float, ivert: str, ihorz: str = 'NAD83_2011', iunit: str = 'm', geoid: str = 'geoid12b', overt: str = 'NAVD88', ounit: str = 'm'):
    url_str = f'https://vdatum.noaa.gov/vdatumweb/api/tidal?lon={longitude}&lat={latitude}' \
              + f'&height={elevation}&s_h_frame={ihorz}&s_v_frame={ivert}&s_v_unit={iunit}' \
              + f'&t_v_frame={overt}&t_v_unit={ounit}'
    vd_value = requests.get(url = url_str).content.decode()
    new = pd.read_json(vd_value, lines = True)
    if 'errorCode' in new.columns:
    	new.insert(0,'tar_height','NaN')
    return new