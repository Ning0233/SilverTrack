import { render, screen } from '@testing-library/react';
import App from './App';

test('renders SilverTrack brand', () => {
  render(<App />);
  const brand = screen.getByText(/SilverTrack/i);
  expect(brand).toBeInTheDocument();
});
