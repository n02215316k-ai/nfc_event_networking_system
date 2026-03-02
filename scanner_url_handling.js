
// Update the processScan function in scanner.html to handle both formats:

function processScan(scannedData, method) {
    let userId = null;
    
    // Format 1: Full URL (https://domain.com/profile/user/123)
    if (scannedData.includes('/profile/user/')) {
        userId = scannedData.split('/profile/user/')[1].split('?')[0];
    }
    // Format 2: USER:123|URL:...
    else if (scannedData.includes('USER:')) {
        const parts = scannedData.split('|');
        userId = parts[0].split('USER:')[1];
    }
    // Format 3: Just the ID
    else if (!isNaN(scannedData)) {
        userId = scannedData;
    }
    // Format 4: Try to extract ID from any URL
    else if (scannedData.includes('http')) {
        const match = scannedData.match(/\/(\d+)(?:\?|$)/);
        if (match) userId = match[1];
    }
    
    if (!userId) {
        showScanResult('danger', 'Invalid scan data format');
        return;
    }
    
    // Rest of the processing code...
}
