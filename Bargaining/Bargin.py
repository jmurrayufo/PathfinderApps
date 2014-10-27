#!/usr/bin/env python

import Funcs
import numpy as np
import os
import time

GlobalDecimalRounding = 4

DEBUG = False

class Object(object):
   pass

class bcolors:
   BLACK = '\033[30m'
   RED = '\033[31m'
   GREEN = '\033[32m'
   YELLOW = '\033[33m'
   BLUE = '\033[34m'
   MAGENTA = '\033[35m'
   CYAN = '\033[36m'
   WHITE = '\033[37m'
   
   BLACKI = '\033[90m'
   REDI = '\033[91m'
   GREENI = '\033[92m'
   YELLOWI = '\033[93m'
   BLUEI = '\033[94m'
   MAGENTAI = '\033[95m'
   CYANI = '\033[96m'
   WHITEI = '\033[97m'

   BBLACK = '\033[40m'
   BRED = '\033[41m'
   BGREEN = '\033[42m'
   BYELLOW = '\033[43m'
   BBLUE = '\033[44m'
   BMAGENTA = '\033[45m'
   BCYAN = '\033[46m'
   BWHITE = '\033[47m'
   
   BBLACKI = '\033[100m'
   BREDI = '\033[101m'
   BGREENI = '\033[102m'
   BYELLOWI = '\033[103m'
   BBLUEI = '\033[104m'
   BMAGENTAI = '\033[105m'
   BCYANI = '\033[106m'
   BWHITEI = '\033[107m'

   RESET = '\033[0m'


class BargainSM(object):
   

   def __init__( self ):
      self.Seller = Object()
      
      self.Buyer = Object()
      self.Buyer.Name = "NPCBob"

      self.Item = Object()

      self.State = 0

      self.Result = None


   def Run( self ):
      
      stateMap = [ 
         self.Step0,
         self.Step1,
         self.Step2,
         self.Step3,
         self.Step4,
         self.Step5,
         ]

      while self.State < len( stateMap ) :
         try :
            stateMap[ self.State ]()
         except (KeyboardInterrupt) :
            print "\nYou have exited the script execution."
            print "Would you like to go back or quit?"
            print "q: Quit"
            print "b: Go back one state and continue" 
            print "r: Restart Current State and continue"
            userSel = raw_input("> ")
            if userSel == 'b' and self.State > 0:
               self.State -= 1
               continue

            elif userSel == 'r' :
               continue

            else :
               break
         if self.Result != None :
            self.StepFinished()
            break

         self.State += 1

   def Step0( self ):
      os.system('clear')

      """
      Step 0: Get data for this run!
      """

      print "Welcome to the Bargaining Simulator!"
      print "   Please note that this application is in TESTING at this time"
      print "   Many options are not easy to \"undo\" and can result in odd results!"

      print "Whos is trying to Bargain today?"
      self.Seller.Name = raw_input( "> " )

      print "And what level are they?"
      self.Seller.Level = Funcs.GetLegalInt( "> " )

      print 
      print "What is the name of the item to be sold?"
      self.Item.Name = raw_input( "> " )


      print "Players: What did you appraise this item at?"
      self.Item.AppraisedAt = Funcs.GetLegalFloat()

      print bcolors.RED,
      print "   DM: What is the REAL value of this item in the current market?"
      self.Item.Worth = Funcs.GetLegalFloat()

      print "   DM: What is the DC check to apprise this item?"
      print "      NOTE: This is 20 for most things, with a +5 if it is rare or exotic"
      self.Item.AppraiseDC = Funcs.GetLegalInt()

      tmpProbSet = np.linspace( 1, 5, 5) / sum( np.linspace( 1, 5, 5 ) )
      self.Buyer.SkillsList = np.random.choice( Funcs.SkillChecks( self.Seller.Level ), 3, replace = True,  p = tmpProbSet )
      self.Buyer.BluffSkill = self.Buyer.SkillsList[0]
      self.Buyer.AppraiseSkill = self.Buyer.SkillsList[1]
      self.Buyer.SenseMotiveSkill = self.Buyer.SkillsList[2]

      self.Buyer.CHAModifier = np.random.choice( Funcs.Attribute( self.Seller.Level ), p = tmpProbSet )


      print "   DM: The Buyer has been shuffled in the background, and got these stats!"
      print "   Buyer Bluff: {}".format( self.Buyer.BluffSkill )
      print "   Buyer Appraise: {}".format( self.Buyer.AppraiseSkill )
      print "   Buyer Sense Motive: {}".format( self.Buyer.SenseMotiveSkill )
      print "   Buyer CHA: {}".format( self.Buyer.CHAModifier )

      print bcolors.RESET


   def Step1( self ):
      """
      Step 1: Seller Sets the Asking Price
      The seller suggests a price to the self.Buyer. If the Asking Price is more than 150%% of the item's actual value, the buyer simply refuses to bargain. The lowest amount the seller will accept is 75%% of this Asking Price.
      """

      print 
      print "{} is trying to sell a \"{}\" to {}.".format( self.Seller.Name, self.Item.Name, self.Buyer.Name)
      print "This item was appriased at {:,.2f} gp".format( self.Item.AppraisedAt )

      print "What is the Seller Offering for an Asking Price?"
      self.Seller.AskingPrice = Funcs.GetLegalInt()
      print "Your asking for {} gp".format( self.Seller.AskingPrice )


   def Step2( self ):

      """
      Step 2: Evaluate Item
      The buyer chooses to attempt either an Appraise check to estimate the item's value or a Sense Motive check opposed by the seller's Bluff check (with failure meaning the buyer believes the seller is being fair). If the seller's price is the same as the buyer's estimation of the item's value, no Sense Motive check is needed and the buyer believes the self.Seller.

      A group of items can be sold as a unit. If the buyer is dealing with a mix of items she can appraise and others she can only guess about, she uses either Appraise or Sense Motive, depending on which she has more skill ranks in.

      The GM can allow a PC to substitute an appropriate Knowledge skill for Appraise or Sense Motive, such as Knowledge (arcana) for selling a rare book about magic. He may also assign modifiers to skill checks to reflect expertise or ignorance about a specific type of item, good roleplaying, or insulting behavior toward an NPC buyer or self.Seller.
      """

      # Get evaluation from the Buyer on the items worth
      """
         A DC 20 Appraise check determines the value of a common self.Item. If you succeed by 5 or more, you also determine if the item has magic properties, although this success does not grant knowledge of the magic item's abilities. If you fail the check by less than 5, you determine the price of that item to within 20%% of its actual value. If you fail this check by 5 or more, the price is wildly inaccurate, subject to GM discretion. Particularly rare or exotic items might increase the DC of this check by 5 or more.

         You can also use this check to determine the most valuable item visible in a treasure hoard. The DC of this check is generally 20 but can increase to as high as 30 for a particularly large hoard.
      """


      print
      print "Will {} (The Buyer) trust their appraisal skill of {}?".format( self.Buyer.Name, self.Buyer.AppraiseSkill )
      self.Buyer.UseAppraiseSkill = Funcs.GetTruth()

      print
      print "Does {} (The Seller) want to attempt to bluff the Buyer into believeing their asking price is fair?".format( self.Seller.Name )
      self.Seller.UseBluffOnItemWorth = Funcs.GetTruth()

      if self.Seller.UseBluffOnItemWorth :
         print "What is the total result of {}'s bluff check?".format( self.Seller.Name )
         self.Seller.BluffCheck = Funcs.GetLegalInt()


      print
      self.Buyer.AppraiseCheck = Funcs.D20() + self.Buyer.AppraiseSkill - self.Item.AppraiseDC
      print bcolors.RED + "{Name} got a {AppraiseCheck} on their Appraise check for the item".format( **self.Buyer.__dict__ )
      print "   Note: This is the Roll + Mods - DC!"

      # Check was passed, Buyer knows the value of the item
      if self.Buyer.AppraiseCheck >= 0 :
         print "{Name} understands the items worth well".format( **self.Buyer.__dict__ )
         self.Buyer.ValueEstimation = self.Item.Worth

      # Check was failed by just a bit, Buyer knows the value within 20%
      elif self.Buyer.AppraiseCheck >= -5 :
         print "{Name} only partially understands the value of the item!".format( **self.Buyer.__dict__ )
         self.Buyer.ValueEstimation = int( self.Item.Worth * np.random.uniform( 0.8, 1.2 ) )

      # Buyer has very wide range of estimation!
      else:
         print "{Name} has no clue about the value of the item!!!".format( **self.Buyer.__dict__ )   
         self.Buyer.ValueEstimation = int( self.Item.Worth * np.random.uniform( 0.2, 1.8 ) )

      self.Buyer.ValueEstimation = Funcs.Round_to_n( self.Buyer.ValueEstimation, GlobalDecimalRounding )
      print "   They estimate this value at {:,.2f}".format( self.Buyer.ValueEstimation )

      self.Buyer.ThinksSheIsBeingLiedTo = False
      self.Buyer.SucessfullyBluffed = False

      print 
      # The Buyer will use their own estimations 
      if self.Buyer.UseAppraiseSkill :

         print "{Name} will trust their own Appraisal of the item".format( **self.Buyer.__dict__ )
         self.Buyer.ValueEstimation = self.Buyer.ValueEstimation
         if self.Seller.AskingPrice < self.Buyer.ValueEstimation :
            print "   {} is asking for less then the Buyer thinks the item is worth. ".format( self.Seller.Name )

      else :
         # Buyer will attempt to Sense Motive on the Seller to get an idea of the value
         #  of the self.Item. 

         # If the Seller offered within 1% of the true value, just take that
         if abs( self.Buyer.ValueEstimation - self.Seller.AskingPrice ) < self.Buyer.ValueEstimation * 0.01 :
            print "{} has been talked into thinking the {} is offering a fair value on the self.Item.".format( self.Buyer.Name, self.Seller.Name )
            self.Buyer.ValueEstimation = self.Seller.AskingPrice
         elif self.Seller.UseBluffOnItemWorth :
            print "{} is trying to bluff {}!".format( self.Seller.Name, self.Buyer.Name )
            Broll = Funcs.D20() + self.Buyer.SenseMotiveSkill
            Sroll = self.Seller.BluffCheck 
            print "   Buyer Sense Motive:",Broll
            print "         Seller Bluff:",Sroll
            if Sroll > Broll :
               print "   {} succesfully bluffed {} into their estimation of the item".format( self.Seller.Name, self.Buyer.Name )
               print "   They agree that its probably worth around {:,.2f} gp".format( self.Seller.AskingPrice )
               self.Buyer.ValueEstimation = self.Seller.AskingPrice
               self.Buyer.SucessfullyBluffed = True
            
            # Oh no! The Buyer knows she is being lied too!
            else :
               print "   {} fail to bluffed {} into their estimation of the item!".format( self.Seller.Name, self.Buyer.Name )
               print "   {Name} suspects they are being lied too!!!".format( **self.Buyer.__dict__ )
               print "   They will use their own estimations of {:,.2f} gp".format( self.Buyer.ValueEstimation )
               if self.Seller.AskingPrice < self.Buyer.ValueEstimation :
                  print "      NOTE: The player has offered the NPC even LESS then they think it is worth!"
                  print "         They will use the players value for all other negotiations!"
               self.Buyer.ValueEstimation = self.Buyer.ValueEstimation
               self.Buyer.ThinksSheIsBeingLiedTo = True
         else :
            print "{} didn't try to bluff, {} will keep their estimation!".format( self.Seller.Name, self.Buyer.Name )

      print bcolors.RESET

      if self.Seller.AskingPrice > self.Buyer.ValueEstimation * 1.5 :
         print "The buyer is insulted! They will not deal with you again!"
         exit()


   def Step3( self ):
      """
      Step 3: Determine Undercut
      The Undercut Percentage is a portion of the item's price or value used to determine the buyer's Initial and Final Offers.

      To determine the Undercut Percentage, have the buyer attempt a Bluff check opposed by the seller's Sense Motive check. The Undercut Percentage is 2%%, plus 1%% for every point by which the Bluff check exceeds the Sense Motive check (minimum 0%%).
      """

      self.Buyer.BluffCheck = Funcs.D20() + self.Buyer.BluffSkill

      print
      print "{} is trying to haggle {} on undercut amounts.".format( self.Buyer.Name, self.Seller.Name)
      print "{Name} needs to sense motive to try to keep this undercut down!".format( **self.Seller.__dict__ )
      print "What is {Name}'s Sense Motive check?".format( **self.Seller.__dict__ )
      self.Seller.SenseMotiveCheck = Funcs.GetLegalInt()

      UndercutMod = max( 0, self.Buyer.BluffCheck - self.Seller.SenseMotiveCheck )

      print
      print bcolors.RED + \
         "{Name} bluffs with a {BluffCheck}".format( **self.Buyer.__dict__ ) + \
         bcolors.RESET
      print "{Name} Senses Motive with a {SenseMotiveCheck}".format( **self.Seller.__dict__ )

      self.Buyer.UndercutPercent = 0.02 + ( 0.01 * UndercutMod )

      print "This results in a total undercut of: {:2.0%}".format( self.Buyer.UndercutPercent )


   def Step4( self ):
      """
      Step 4: Set Offers
      The Initial Offer is the buyer's first counteroffer to the seller's Asking Price. The Final Offer is the largest amount the buyer is willing to pay. Though the seller and buyer negotiate back and forth, the buyer won't exceed this offer. For example, if the seller's Asking Price is 1,000 gp, the buyer's Initial Offer may be 800 gp and the Final Offer 900 gp. These offers are determined by how much the buyer thinks the item is worth compared to the seller's Asking Price.

      Fair (Appraise or Sense Motive): If the seller's Asking Price is less than or equal to the amount that the buyer thinks the item is worth, subtract the Undercut Percentage from the seller's price to get the Final Offer, and subtract 2 x the Undercut Percentage to get the Initial Offer.

      Unfair (Appraise): If the result of the buyer's Appraise check leads her to believe the item is worth less than the seller's Asking Price, subtract the Undercut Percentage from the buyer's estimate of the item's value to get the Final Offer, and subtract 2 x the Undercut Percentage to get the Initial Offer.

      Unfair (Sense Motive): If the result of the buyer's Appraise check leads her to believe the seller's Asking Price is too high, subtract 2 x the Undercut Percentage from the seller's Asking Price to get the Final Offer, and subtract 4 x the Undercut Percentage to get the Initial Offer.
      """

      print bcolors.RED
      # Buyer thinks the asking price is fair, and takes it.
      if self.Seller.AskingPrice <= self.Buyer.ValueEstimation :
         print "{} thinks the offer is fair at {:,.2f}".format( self.Buyer.Name, min( self.Seller.AskingPrice, self.Buyer.ValueEstimation ) )
         self.Buyer.FinalOffer = self.Seller.AskingPrice * ( 1 - self.Buyer.UndercutPercent )
         self.Buyer.InitialOffer = self.Seller.AskingPrice * ( 1 - self.Buyer.UndercutPercent * 2 )

      # The Buyer doesn't think she is offered fair value
      else:
         # The PC bluffed them anyway, and the Buyer adjusts their offers to match
         if self.Buyer.SucessfullyBluffed :
            print "{} fell for the bluff, and thinks the offer is fair at {:,.2f} gp".format( self.Buyer.Name, min( self.Seller.AskingPrice, self.Buyer.ValueEstimation ) )
            self.Buyer.FinalOffer = self.Seller.AskingPrice * ( 1 - self.Buyer.UndercutPercent )
            self.Buyer.InitialOffer = self.Seller.AskingPrice * ( 1 - self.Buyer.UndercutPercent * 2 )
         # If the Buyer was not bluffed, AND they know that they were bluffed, cut into thir own estimation more.
         if not self.Buyer.SucessfullyBluffed and self.Buyer.ThinksSheIsBeingLiedTo :
            print "{} thinks they are being lied too!!! They lower thier offer to {:,.2f} gp".format( self.Buyer.Name, self.Buyer.ValueEstimation )
            self.Buyer.FinalOffer = self.Buyer.ValueEstimation * ( 1 - self.Buyer.UndercutPercent * 2 )
            self.Buyer.InitialOffer = self.Buyer.ValueEstimation * ( 1 - self.Buyer.UndercutPercent * 4 )
         
         # Else the Buyer was neither lied to, nor thinks they are being lied too. 
         else:
            print "{} doesn't think that the item is really worth so much, and lowers their offer to {:,.2f} gp!".format( self.Buyer.Name, self.Buyer.ValueEstimation )
            self.Buyer.FinalOffer = self.Buyer.ValueEstimation * ( 1 - self.Buyer.UndercutPercent )
            self.Buyer.InitialOffer = self.Buyer.ValueEstimation * ( 1 - self.Buyer.UndercutPercent * 2 )


      print 
      print "We will now salt the Final and Initial Offers to keep players from outright calculating values!"
      print "We will pick a salt amount between -1% and +1% and adjust both offers by the same %"

      salt = 1.0 + np.random.uniform( -0.01, 0.01 )

      # Salt helps keeps things fun, and prevent any meta-gaming. This is a very minor shift, but prevents players from gaming the system too much. 
      self.Buyer.FinalOffer *= salt
      self.Buyer.InitialOffer *= salt

      print bcolors.RESET,

      self.Buyer.FinalOffer = Funcs.Round_to_n( self.Buyer.FinalOffer, GlobalDecimalRounding )
      self.Buyer.InitialOffer = Funcs.Round_to_n( self.Buyer.InitialOffer, GlobalDecimalRounding )


   def Step5( self ):
      """
      Step 5: Bargain
      The buyer begins bargaining by countering the seller's price with her Initial Offer. This step repeats until the buyer and seller agree on a price or one side ends negotiations.

      Counteroffer Is Less Than Final Offer: If the seller counters with a price that is less than the buyer's Final Offer, have the seller attempt a Diplomacy check (DC 15 + the buyer's Charisma modifier). Success means the buyer accepts the seller's counteroffer and buys the self.Item. Failure means the buyer holds at her Initial Offer. The seller can try again, but the Diplomacy check DC increases by 5 unless the seller lowers his price.
      HOUSERULE: A offer less then the final offer SHOULD result in a counter offer!

      Counteroffer Equals Final Offer: If the seller counters with a price that is the same as the buyer's Final Offer, have the seller attempt a Diplomacy check (20 + the buyer's Charisma modifier). Success means the buyer accepts the seller's counteroffer and buys the self.Item. Failure means the buyer counteroffers at a price between the Initial Offer and the Final Offer. The seller can try again, but the Diplomacy DC increases by 5 unless the seller lowers his price.

      Counteroffer Exceeds Final Offer: If the seller counters with a price higher than the buyer's Final Offer, have the seller attempt a Diplomacy check (25 + the buyer's Charisma modifier). Success means the buyer counteroffers at a price between the Initial Offer and the Final Offer. Failure means the buyer holds at her Initial Offer. Failure by 5 or more means the buyer is insulted and lowers her offer or refuses to deal with the self.Seller. The seller can try again, but the Diplomacy DC increases by 5 unless the seller lowers his price.
      """

      print
      print "{} will make an initial offer of {:,.2f} gp".format( self.Buyer.Name, self.Buyer.InitialOffer )

      if self.Buyer.InitialOffer < self.Seller.AskingPrice * 0.75 :
         print "   WARNING! The buy is asking for {:.1%} of the asking price! This is less then 75% of the asking price".format( self.Buyer.InitialOffer / self.Seller.AskingPrice )
      else :
         print "   Buyer is asking for {:.1%} of the asking price! ".format( self.Buyer.InitialOffer / self.Seller.AskingPrice )

      print

      self.Buyer.CurrentOffer = self.Buyer.InitialOffer
      self.Seller.CurrentOffer = self.Seller.AskingPrice

      # Used to keep track of failures to negotiate price!
      failedOfferDCMod = 0

      lastFailedPrice = None

      while 1 :
         print
         if DEBUG : print "Buyer.FinalOffer:",Buyer.FinalOffer
         if DEBUG : print "Buyer.InitialOffer:",Buyer.InitialOffer
         print "{} is currently offering a price of {:,.2f} gp".format( self.Buyer.Name, self.Buyer.CurrentOffer )
         if lastFailedPrice :
            print "Your last failing price was {:,.2f}".format( lastFailedPrice )
            if lastFailedPrice <= self.Buyer.CurrentOffer :
               print "The buyer, upon futher consideration, thinks you offer is fair, and takes it!"
               self.Seller.CurrentOffer = lastFailedPrice
               break
         print "What is {}'s counter offer?".format( self.Seller.Name )
         self.Seller.CurrentOffer = Funcs.GetLegalFloat()

         if self.Seller.CurrentOffer < self.Buyer.CurrentOffer :
            print "Are you SURE that {} wants to offer {:,.2f}?".format( self.Seller.Name, self.Seller.CurrentOffer )
            print "{} is offering {:,.2f} already!".format( self.Buyer.Name, self.Buyer.CurrentOffer )
            if Funcs.GetTruth() :
               break
            else :
               continue

         if self.Seller.CurrentOffer == self.Buyer.CurrentOffer :
            break

         if lastFailedPrice and self.Seller.CurrentOffer < lastFailedPrice :
            print bcolors.RED + "You offered a new lower price. DC reset!" + bcolors.RESET
            lastFailedPrice = None
            failedOfferDCMod = 0

         # The Seller hasn't gone bellow the Buyer, or met her, so we will need to roll a diplimacy no mater what happens!
         print
         print "{} is considering the offer, roll a diplomacy!".format( self.Buyer.Name )
         roll = Funcs.GetLegalInt()


         # NOTE: This is out of normal ordering! 
         #  This ordering differece is here to detect offers with 1% of the final offer anyway, and try to take them FIRST. 
         if abs( self.Seller.CurrentOffer - self.Buyer.FinalOffer ) < self.Buyer.FinalOffer * 0.01 :

            if roll >= 20 + self.Buyer.CHAModifier + failedOfferDCMod :
               break
            
            # Only check for failure if we are actaully OVER that value!
            elif self.Seller.CurrentOffer >= self.Buyer.FinalOffer :
               self.Buyer.CurrentOffer = np.random.uniform( self.Buyer.CurrentOffer, self.Buyer.FinalOffer )
               self.Buyer.CurrentOffer = Funcs.Round_to_n( self.Buyer.CurrentOffer, GlobalDecimalRounding )

               lastFailedPrice = max( lastFailedPrice, self.Seller.CurrentOffer )
               failedOfferDCMod += 5
               print "Negotiations fail, the DC is now",failedOfferDCMod
               print "{} will need to lower thier price bellow {:,.2f} gp to be rid of this DC.".format( self.Seller.Name, lastFailedPrice )
               print "{} is now offering {:,.2f} gp for the self.Item.".format( self.Buyer.Name, self.Buyer.CurrentOffer )
               continue


         # The Seller is asking for a price between the Initial and Final Offer
         if self.Seller.CurrentOffer < self.Buyer.FinalOffer :

            # Check to see if this offer is just outright accepted
            diplomacyDC = 15 + self.Buyer.CHAModifier + failedOfferDCMod
            if roll >= diplomacyDC :
               break
            print bcolors.RED,
            print "   DM: The player did not beat a check of {} with a roll of {}".format( diplomacyDC, roll ),
            print bcolors.RESET

            lastFailedPrice = self.Seller.CurrentOffer
            failedOfferDCMod += 5
            print "Negotiations failed, the DC is now: ",failedOfferDCMod
            print "{} will need to lower thier price bellow {:,.2f} gp to be rid of this DC.".format( self.Seller.Name, lastFailedPrice )
            if roll - diplomacyDC >= -10 :
               # Calculate new counter offer from the Buyer
               self.Buyer.CurrentOffer = np.random.uniform(
                  self.Buyer.CurrentOffer*1.001,
                  ( self.Buyer.CurrentOffer + self.Seller.CurrentOffer ) / 2
                  )

               self.Buyer.CurrentOffer = Funcs.Round_to_n( self.Buyer.CurrentOffer, GlobalDecimalRounding )

               if self.Buyer.CurrentOffer >= self.Seller.CurrentOffer :
                  print "{} Reconsiders your offer, and finds it to be fair.".format( self.Buyer.Name )
                  exit()

               print "{} counteroffers at {:,.2f} gp for the self.Item.".format( self.Buyer.Name, self.Buyer.CurrentOffer )
            continue


         elif self.Seller.CurrentOffer > self.Buyer.FinalOffer :
            # Success
            diplomacyDC = 25 + self.Buyer.CHAModifier + failedOfferDCMod
            if roll >= diplomacyDC :
               self.Buyer.CurrentOffer = np.random.uniform( self.Buyer.InitialOffer, self.Buyer.FinalOffer )
               self.Buyer.CurrentOffer = Funcs.Round_to_n( self.Buyer.CurrentOffer, GlobalDecimalRounding )
               print "{} wont go that high, and counter offers with {:,.2f} gp".format( self.Buyer.Name, self.Buyer.CurrentOffer )
            
            # Failure by only 5
            elif roll + 5 >= diplomacyDC :
               print "{} refuses the current offer, and re-offers the initial price of {:,.2f} gp".format( self.Buyer.Name, self.Buyer.InitialOffer )
               self.Buyer.CurrentOffer = self.Buyer.InitialOffer

               lastFailedPrice = self.Seller.CurrentOffer
               failedOfferDCMod += 5
               print "Negotiations fail, the DC is now",failedOfferDCMod
               print "{} will need to lower thier price bellow {:,.2f} gp to be rid of this DC.".format( self.Seller.Name, lastFailedPrice )

            # SHIT! Failed by more then 5!
            else :
               # TODO: 1D Interpolation from 100% -> 0 to 150% -> 20 for 
               print 
               print "Wo! {} is VERY upset about this offer! The players diplimacy skill needs to keep them at the table!".format( self.Buyer.Name )
               overshootDC = int( np.interp( self.Seller.CurrentOffer, [Buyer.FinalOffer, self.Buyer.FinalOffer*1.5], [0,20] ) )
               print bcolors.RED,
               print "   DM: The DC to beat is {}+{}={}".format( overshootDC, failedOfferDCMod, overshootDC + failedOfferDCMod ),
               print bcolors.RESET

               if roll < overshootDC + failedOfferDCMod :

                  print bcolors.RED,
                  print "The final DC was {} (Overshoot) + {} (mod) = {}".format( overshootDC, failedOfferDCMod, overshootDC+failedOfferDCMod )
                  print "{} is greatly offended by the offer! They refuse to continue dealing with {}!".format( self.Buyer.Name, self.Seller.Name )
                  exit()
               adjustment = np.random.uniform( 0.01, 0.09 )
               print "{} is insulted by the offer! They lower their offer by {:.0%}!".format( self.Buyer.Name, adjustment )
               self.Buyer.InitialOffer = Funcs.Round_to_n( self.Buyer.InitialOffer * ( 1 - adjustment ), GlobalDecimalRounding )
               self.Buyer.FinalOffer = Funcs.Round_to_n( self.Buyer.FinalOffer * ( 1 - adjustment ), GlobalDecimalRounding )
               self.Buyer.CurrentOffer = self.Buyer.InitialOffer

               lastFailedPrice = self.Seller.CurrentOffer
               failedOfferDCMod += 5
               print "Negotiations fail, the DC is now",failedOfferDCMod
               print "{} will need to lower thier price bellow {:,.2f} gp to be rid of this DC.".format( self.Seller.Name, lastFailedPrice )


   def StepFinished( self ):

      print          
      print "SUCCESS! The price is agreed!"
      print "{} will pay {:,.2f} gp for the item!".format( self.Buyer.Name, self.Seller.CurrentOffer )


x = BargainSM()

x.Run()