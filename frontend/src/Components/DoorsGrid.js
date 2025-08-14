import React, { useState } from 'react';
import { HotTable } from '@handsontable/react';
import 'handsontable/dist/handsontable.full.min.css';

const DoorsGrid = () => {
  const [data, setData] = useState([
    ['Door 1', 'Timber', 'Single Leaf', 'Fire-rated'],
    ['Door 2', 'Steel', 'Double Leaf', 'Non-rated']
  ]);

  const handleSave = () => {
    fetch('http://localhost:8000/api/save-doors/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ doors: data })
    })
      .then(response => {
        if (response.ok) {
          alert('Doors saved successfully!');
        } else {
          alert('Failed to save.');
        }
      })
      .catch(error => {
        console.error('Error saving doors:', error);
        alert('Error occurred while saving.');
      });
  };

  return (
    <div>
      <HotTable
        data={data}
        colHeaders={['Door', 'Material', 'Type', 'Rating']}
        rowHeaders={true}
        width="100%"
        height="300"
        licenseKey="non-commercial-and-evaluation"
        afterChange={(changes, source) => {
          if (source === 'edit') {
            setData([...data]); // re-trigger state
          }
        }}
      />
      <button onClick={handleSave}>Save to Backend</button>
    </div>
  );
};

export default DoorsGrid;
