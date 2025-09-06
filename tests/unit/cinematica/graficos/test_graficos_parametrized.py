import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from cinetica.cinematica.rectilineo.movimiento_rectilineo_uniforme import MovimientoRectilineoUniforme
from cinetica.cinematica.rectilineo.movimiento_rectilineo_uniformemente_variado import MovimientoRectilineoUniformementeVariado
from cinetica.cinematica.circular.movimiento_circular_uniforme import MovimientoCircularUniforme
from cinetica.cinematica.espacial.movimiento_espacial import MovimientoEspacial
from cinetica.cinematica.graficos.graficador import (
    plot_mru,
    plot_mruv,
    plot_mcu,
    plot_movimiento_espacial,
    configurar_estilo_grafico,
)
from cinetica.units import ureg, Q_


class TestPlottingParametrized:
    """Parametrized tests for plotting functions with various motion configurations."""

    @pytest.mark.parametrize("pos_inicial, vel_inicial, tiempo_max, num_puntos", [
        (0, 10, 5, 50),
        (5, -3, 8, 80),
        (20, 0, 10, 100),
        (-10, 15, 6, 60),
    ])
    @patch('cinetica.cinematica.graficos.graficador.plt')
    def test_plot_mru_parametrized(self, mock_plt, pos_inicial, vel_inicial, tiempo_max, num_puntos):
        """Test MRU plotting with various parameters."""
        # Setup mock
        mock_fig = Mock()
        mock_axs = [Mock(), Mock()]  # Array of mock axes for subplots
        mock_plt.subplots.return_value = (mock_fig, mock_axs)
        
        # Create MRU object
        mru = MovimientoRectilineoUniforme(
            posicion_inicial=pos_inicial * ureg.meter,
            velocidad_inicial=vel_inicial * ureg.meter / ureg.second
        )
        
        # Call plotting function
        plot_mru(mru, tiempo_max * ureg.second, num_puntos)
        
        # Verify that subplots were created and plotting functions were called
        mock_plt.subplots.assert_called_once()
        mock_plt.show.assert_called_once()

    @pytest.mark.parametrize("pos_inicial, vel_inicial, aceleracion, tiempo_max", [
        (0, 0, 10, 3),  # Free fall from rest
        (10, 20, -5, 4),  # Deceleration
        (5, -10, 2, 6),  # Negative initial velocity
        (0, 15, 0, 5),  # Zero acceleration (MRU case)
    ])
    @patch('cinetica.cinematica.graficos.graficador.plt')
    def test_plot_mruv_parametrized(self, mock_plt, pos_inicial, vel_inicial, aceleracion, tiempo_max):
        """Test MRUV plotting with various parameters."""
        # Setup mock
        mock_fig = Mock()
        mock_axs = [Mock(), Mock(), Mock()]  # Array of mock axes for 3 subplots
        mock_plt.subplots.return_value = (mock_fig, mock_axs)
        
        # Create MRUV object
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=pos_inicial * ureg.meter,
            velocidad_inicial=vel_inicial * ureg.meter / ureg.second,
            aceleracion_inicial=aceleracion * ureg.meter / ureg.second**2
        )
        
        # Call plotting function
        plot_mruv(mruv, tiempo_max * ureg.second)
        
        # Verify that subplots were created and plotting functions were called
        mock_plt.subplots.assert_called_once()
        mock_plt.show.assert_called_once()

    @pytest.mark.parametrize("radio, vel_angular, tiempo_max, num_points", [
        (5, 2, 10, 50),
        (10, 1.5, 8, 60),
        (3, 4, 6, 40),
        (8, 0.5, 12, 80),
    ])
    @patch('cinetica.cinematica.graficos.graficador.plt')
    def test_plot_mcu_parametrized(self, mock_plt, radio, vel_angular, tiempo_max, num_points):
        """Test MCU plotting with various parameters."""
        # Setup mock
        mock_fig = Mock()
        mock_axs = [Mock(), Mock(), Mock()]  # Array of mock axes for 3 subplots
        mock_plt.subplots.return_value = (mock_fig, mock_axs)
        
        # Create MCU object
        mcu = MovimientoCircularUniforme(
            radio=radio * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=vel_angular * ureg.radian / ureg.second
        )
        
        # Call plotting function
        plot_mcu(mcu, tiempo_max * ureg.second, num_points)
        
        # Verify that subplots were created and plotting functions were called
        # MCU plotting creates one subplot figure and one standalone figure
        mock_plt.subplots.assert_called_once()
        mock_plt.figure.assert_called_once()
        # MCU plotting shows two figures, so show is called twice
        assert mock_plt.show.call_count == 2

    @pytest.mark.parametrize("tiempo_max, velocidad_components, num_puntos", [
        (4, [5, 3, 0], 50),  # 2D motion in XY plane
        (6, [2, 4, 1], 60),  # 3D motion
        (5, [0, 10, 0], 50),  # Motion along Y axis
        (8, [-3, 2, -1], 60),  # Negative velocity components
    ])
    @patch('cinetica.cinematica.graficos.graficador.plt')
    def test_plot_movimiento_espacial_parametrized(self, mock_plt, tiempo_max, velocidad_components, num_puntos):
        """Test spatial motion plotting with various parameters."""
        # Setup mock
        mock_fig = Mock()
        mock_axs = Mock()  # Single axis for spatial motion plot
        mock_plt.subplots.return_value = (mock_fig, mock_axs)
        
        # Create spatial movement object (ensure 3D vectors)
        posicion_inicial = [0, 0, 0]  # Always 3D
        velocidad_inicial = velocidad_components  # Already 3D from parametrize
        
        espacial = MovimientoEspacial(
            posicion_inicial=posicion_inicial,
            velocidad_inicial=velocidad_inicial
        )
        
        # Call plotting function
        plot_movimiento_espacial(espacial, tiempo_max * ureg.second)
        
        # Verify that figure was created and plotting functions were called
        mock_plt.figure.assert_called_once()
        mock_plt.show.assert_called_once()


class TestPlottingErrorHandling:
    """Parametrized tests for plotting error handling."""

    @pytest.mark.parametrize("tiempo_max, expected_error", [
        (-1, ValueError),
        (0, ValueError),
        (-5, ValueError),
    ])
    def test_plot_functions_negative_time_error(self, tiempo_max, expected_error):
        """Test that plotting functions raise errors for invalid time values."""
        mru = MovimientoRectilineoUniforme(
            posicion_inicial=0 * ureg.meter,
            velocidad_inicial=5 * ureg.meter / ureg.second
        )
        
        with pytest.raises(expected_error):
            plot_mru(mru, tiempo_max * ureg.second)

    @pytest.mark.parametrize("num_puntos, expected_error", [
        (-10, ValueError),  # Only negative values should raise errors
    ])
    @patch('cinetica.cinematica.graficos.graficador.plt')
    def test_plot_mru_invalid_points_error(self, mock_plt, num_puntos, expected_error):
        """Test that MRU plotting raises errors for invalid number of points."""
        # Setup mock
        mock_fig = Mock()
        mock_axs = [Mock(), Mock()]  # Array of mock axes for subplots
        mock_plt.subplots.return_value = (mock_fig, mock_axs)
        
        mru = MovimientoRectilineoUniforme(
            posicion_inicial=0 * ureg.meter,
            velocidad_inicial=5 * ureg.meter / ureg.second
        )
        
        with pytest.raises(expected_error):
            plot_mru(mru, 5 * ureg.second, num_puntos)



class TestPlottingStyleConfiguration:
    """Parametrized tests for plotting style configuration."""

    @pytest.mark.parametrize("style_params", [
        {"figure.figsize": [12, 8]},
        {"figure.dpi": 150},
        {"lines.linewidth": 3},
        {"font.size": 12},
    ])
    @patch('cinetica.cinematica.graficos.graficador.plt')
    def test_configurar_estilo_grafico_parametrized(self, mock_plt, style_params):
        """Test style configuration with various parameters."""
        # Mock rcParams as a dictionary
        mock_plt.rcParams = {}
        
        # Call configuration function
        configurar_estilo_grafico()
        
        # Verify style.use was called
        mock_plt.style.use.assert_called_once_with("seaborn-v0_8-darkgrid")
        
        # Verify rcParams were set
        expected_params = {
            "figure.figsize": [10, 6],
            "figure.dpi": 100,
            "lines.linewidth": 2,
            "axes.grid": True,
            "grid.linestyle": "--",
            "grid.alpha": 0.7,
            "font.size": 10,
            "axes.titlesize": 11,
        }
        
        for key, value in expected_params.items():
            assert mock_plt.rcParams[key] == value


class TestPlottingDataValidation:
    """Parametrized tests for plotting data validation."""

    @pytest.mark.parametrize("motion_params, tiempo_max, expected_data_points", [
        # MRU cases
        ((0, 10), 5, 50),  # (pos_inicial, vel_inicial), tiempo_max, expected_points
        ((20, -5), 8, 50),
        # MRUV cases - will be tested separately due to different constructor
    ])
    @patch('cinetica.cinematica.graficos.graficador.plt')
    def test_plot_data_consistency_mru(self, mock_plt, motion_params, tiempo_max, expected_data_points):
        """Test that plotted data is mathematically consistent with physics equations."""
        # Setup mock
        mock_fig = Mock()
        mock_axs = [Mock(), Mock()]  # Array of mock axes for subplots
        mock_plt.subplots.return_value = (mock_fig, mock_axs)
        
        pos_inicial, vel_inicial = motion_params
        mru = MovimientoRectilineoUniforme(
            posicion_inicial=pos_inicial * ureg.meter,
            velocidad_inicial=vel_inicial * ureg.meter / ureg.second
        )
        
        # Call plotting function
        plot_mru(mru, tiempo_max * ureg.second, expected_data_points)
        
        # Verify that subplots were created and plotting functions were called
        mock_plt.subplots.assert_called_once()
        mock_plt.show.assert_called_once()

    @pytest.mark.parametrize("radio, vel_angular, tiempo_values", [
        (5, 2, [0, 1, 2, 3]),
        (10, 1.5, [0, 0.5, 1, 1.5, 2]),
        (3, 4, [0, 0.25, 0.5, 0.75, 1]),
    ])
    def test_mcu_physics_consistency(self, radio, vel_angular, tiempo_values):
        """Test that MCU calculations are consistent across different time values."""
        mcu = MovimientoCircularUniforme(
            radio=radio * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=vel_angular * ureg.radian / ureg.second
        )
        
        for t in tiempo_values:
            # Angular position should follow θ = ω*t
            pos_angular = mcu.posicion_angular(t * ureg.second)
            expected_pos = vel_angular * t * ureg.radian
            assert abs(pos_angular - expected_pos) < 1e-10 * ureg.radian
            
            # Tangential velocity should be constant: v = ω*r
            vel_tangencial = mcu.velocidad_tangencial()
            expected_vel = vel_angular * radio * ureg.meter / ureg.second
            assert abs(vel_tangencial - expected_vel) < 1e-10 * ureg.meter / ureg.second
            
            # Centripetal acceleration should be constant: a = ω²*r
            acc_centripeta = mcu.aceleracion_centripeta()
            expected_acc = vel_angular**2 * radio * ureg.meter / ureg.second**2
            assert abs(acc_centripeta - expected_acc) < 1e-10 * ureg.meter / ureg.second**2
