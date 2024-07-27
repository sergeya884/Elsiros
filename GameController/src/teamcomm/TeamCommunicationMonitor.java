package teamcomm;

import com.jogamp.opengl.GLProfile;
import common.ApplicationLock;
import data.Rules;
import teamcomm.data.GameState;
import teamcomm.gui.MainWindow;
import teamcomm.gui.View3DGSV;
import teamcomm.net.GameControlDataReceiver;
import teamcomm.net.SPLStandardMessageReceiverTCM;
import teamcomm.net.logging.LogReplayer;
import teamcomm.net.logging.Logger;

import javax.swing.*;
import java.awt.*;
import java.io.IOException;
import java.net.SocketException;

/**
 * The team communication monitor starts in this class.
 *
 * @author Felix Thielke
 */
public class TeamCommunicationMonitor {

    private static boolean silentMode = false;
    private static boolean gsvMode = false;
    private static boolean forceWindowed = false;

    private static boolean shutdown = false;
    private static final Object shutdownMutex = new Object();

    /**
     * Startup method of the team communication monitor.
     *
     * @param args This is ignored.
     */
    public static void main(final String[] args) {
        GameControlDataReceiver gcDataReceiver = null;
        SPLStandardMessageReceiverTCM receiver = null;

        parseArgs(args);

        // try to acquire the application lock
        final ApplicationLock applicationLock = new ApplicationLock("TeamCommunicationMonitor");
        try {
            if (!applicationLock.acquire()) {
                if (silentMode) {
                    System.out.println("An instance of TeamCommunicationMonitor already exists.");
                } else {
                    JOptionPane.showMessageDialog(null,
                            "An instance of TeamCommunicationMonitor already exists.",
                            "Multiple instances",
                            JOptionPane.WARNING_MESSAGE);
                }
                System.exit(0);
            }
        } catch (IOException | HeadlessException e) {
            if (silentMode) {
                System.out.println("Error while trying to acquire the application lock.");
            } else {
                JOptionPane.showMessageDialog(null,
                        "Error while trying to acquire the application lock.",
                        e.getClass().getSimpleName(),
                        JOptionPane.ERROR_MESSAGE);
            }
            System.exit(-1);
        }

        if (silentMode) {
            System.out.println("Team Communication Monitor was started in silent mode.\nMessages will be received and logged but not displayed.");
        }

        if (!silentMode) {
            // Initialize the JOGL profile for 3D drawing
            GLProfile.initSingleton();
        }

        // Check if the GameController is running
        try {
            final ApplicationLock lock = new ApplicationLock("GameController");
            if (!lock.acquire()) {
                // Do not log messages if a GameController is running on the same system
                Logger.getInstance().disableLogging();
            } else {
                lock.release();
            }
        } catch (IOException e) {
        }

        // Initialize listener for GameController messages
        try {
            gcDataReceiver = new GameControlDataReceiver();
        } catch (SocketException ex) {
            JOptionPane.showMessageDialog(null,
                    "Error while setting up GameController listener.",
                    "SocketException",
                    JOptionPane.ERROR_MESSAGE);
            System.exit(-1);
        }

        // Initialize listeners for robots
        receiver = SPLStandardMessageReceiverTCM.getInstance();

        // Initialize robot view part of the GUI
        System.setProperty("newt.window.icons", "null,null");
        final MainWindow robotView = silentMode || gsvMode ? null : new MainWindow();
        final View3DGSV gsvView = silentMode ? null : (gsvMode ? new View3DGSV(forceWindowed) : null);

        // Start threads
        gcDataReceiver.start();
        receiver.start();

        // Wait for shutdown
        try {
            synchronized (shutdownMutex) {
                while (!shutdown) {
                    shutdownMutex.wait();
                }
            }
        } catch (InterruptedException ex) {
        }

        // Write config file
        Config.getInstance().flush();

        // Release the application lock
        try {
            applicationLock.release();
        } catch (IOException e) {
        }

        // Shutdown threads and clean up
        GameState.getInstance().shutdown();
        receiver.interrupt();
        gcDataReceiver.interrupt();
        if (robotView != null) {
            robotView.terminate();
        }
        if (gsvView != null) {
            gsvView.terminate();
        }
        LogReplayer.getInstance().close();
        Logger.getInstance().closeLogfile();

        // Try to join receiver threads
        try {
            gcDataReceiver.join(1000);
            receiver.join(1000);
        } catch (InterruptedException ex) {
        }

        // Force exit
        System.exit(0);
    }

    private static final String ARG_HELP_SHORT = "-h";
    private static final String ARG_HELP = "--help";
    private static final String ARG_SILENT_SHORT = "-s";
    private static final String ARG_SILENT = "--silent";
    private static final String ARG_GSV = "--gsv";
    private static final String ARG_WINDOWED = "--windowed";
    private static final String ARG_WINDOWED_SHORT = "-w";

    private static final String ARG_LEAGUE_SHORT = "-l";
    private static final String ARG_LEAGUE = "--league";

    private static void parseArgs(final String[] args) {
        for (int i = 0; i < args.length; i++) {
            switch (args[i].toLowerCase()) {
                case ARG_HELP_SHORT:
                case ARG_HELP:
                    System.out.println("Usage: java -jar TeamCommunicationMonitor.jar {options}"
                            + "\n  (-h | --help)                   display help"
                            + "\n  (-l | --league) <league>        select league"
                            + "\n  (-s | --silent)                 start in silent mode"
                            + "\n  (--gsv)                         start as GameStateVisualizer");
                    System.exit(0);
                case ARG_SILENT_SHORT:
                case ARG_SILENT:
                    silentMode = true;
                    break;
                case ARG_WINDOWED_SHORT:
                case ARG_WINDOWED:
                    forceWindowed = true;
                    break;
                case ARG_GSV:
                    gsvMode = true;
                    break;
                case ARG_LEAGUE_SHORT:
                case ARG_LEAGUE:
                    final String leagueName = args[++i];
                    for (final Rules league : Rules.LEAGUES) {
                        if (league.leagueDirectory.equalsIgnoreCase(leagueName)) {
                            Rules.league = league;
                        }
                    }
                    break;
            }
        }
        System.out.println("Starting with:");
        System.out.println("\tleague = " + Rules.league.leagueName);
        System.out.println("\tgsv = " + gsvMode);
        System.out.println("\twindowed = " + forceWindowed);
        System.out.println("\tsilent = " + silentMode);
    }

    /**
     * Shuts down the program by notifying the main thread.
     */
    public static void shutdown() {
        synchronized (shutdownMutex) {
            shutdown = true;
            shutdownMutex.notifyAll();
        }
    }
}
