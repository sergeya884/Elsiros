package controller.action.ui.half;

import common.Log;
import controller.action.ActionType;
import controller.action.GCAction;
import data.states.AdvancedData;
import data.communication.GameControlData;
import data.Rules;
import data.values.GameStates;
import data.values.GameTypes;
import data.values.SecondaryGameStates;


/**
 * @author Michel Bartsch
 * <p>
 * This action means that the half is to be set to the first half.
 */
public class FirstHalfOvertime extends GCAction {
    /**
     * Creates a new FirstHalf action.
     * Look at the ActionBoard before using this.
     */
    public FirstHalfOvertime() {
        super(ActionType.UI);
    }

    /**
     * Performs this action to manipulate the data (model).
     *
     * @param data The current data to work on.
     */
    @Override
    public void perform(AdvancedData data) {
        if (data.firstHalf != GameControlData.C_TRUE || data.secGameState == SecondaryGameStates.PENALTYSHOOT) {
            data.firstHalf = GameControlData.C_TRUE;
            data.secGameState = SecondaryGameStates.OVERTIME;
            data.changeSide();
            data.kickOffTeam = (data.leftSideKickoff ? data.team[0].teamNumber : data.team[1].teamNumber);
            data.gameState = GameStates.INITIAL;
            Log.state(data, "1st Half Extra Time");
        }
    }

    /**
     * Checks if this action is legal with the given data (model).
     * Illegal actions are not performed by the EventHandler.
     *
     * @param data The current data to check with.
     */
    @Override
    public boolean isLegal(AdvancedData data) {
        if (data.gameType == GameTypes.ROUNDROBIN){
            return false;
        }

        if (data.testmode) {
            return true;
        }

        if ((Rules.league.overtime)
                && (data.gameType == GameTypes.PLAYOFF)
                && (data.secGameState == SecondaryGameStates.NORMAL)
                && (data.gameState == GameStates.FINISHED)
                && (data.firstHalf != GameControlData.C_TRUE)
                && (data.team[0].score == data.team[1].score)
                && ((data.team[0].score > 0) ||
                    Rules.league.getClass().getSimpleName().equals("HLSimulationKid") ||
                    Rules.league.getClass().getSimpleName().equals("HLSimulationAdult") ||
                    Rules.league.getClass().getSimpleName().equals("HLSimulationJunior")
                    )) 
                    //Score > 0 is not required for over time according to the HL Rule book
        {
            return true;
        }

        if (data.firstHalf == GameControlData.C_TRUE
                && (data.secGameState == SecondaryGameStates.OVERTIME)) {
            return true;
        }

        return false;
    }
}