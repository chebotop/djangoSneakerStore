import React from 'react';
import {Button} from '@gravity-ui/uikit';
import {createRoot} from 'react-dom/client';
import {ThemeProvider} from '@gravity-ui/uikit';


const SubmitButton = <Button view="action" size="l" />;

import '@gravity-ui/uikit/styles/fonts.css';
import '@gravity-ui/uikit/styles/styles.css';
import {createRoot} from 'rzeact-dom/client';
import {ThemeProvider} from '@gravity-ui/uikit';

const root = createRoot(document.getElementById('root'));
root.render(
  <ThemeProvider theme="light">
    <App />
  </ThemeProvider>,
);

