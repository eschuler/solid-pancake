// Enums.h
//
// Author: Eric Schuler
// 
// Defines basic enums for a Splendor game

#ifndef SPLENDOR_ENUMS_H
#define SPLENDOR_ENUMS_H

namespace splendor
{

  /**
   * Splendor gem 
   */
  enum Gem
  {
   RED   = 0,
   GREEN = 1,
   BLUE  = 2,
   WHITE = 3,
   BLACK = 4,
   GOLD  = 5
  };

  /**
   * Deck tier
   */
  enum Tier
  {
   ONE   = 0,
   TWO   = 1,
   THREE = 2
  };

  /**
   * What the player chose to do with their turn
   */
  enum TurnOption
  {
   PURCHASE_CARD = 0,
   TAKE_GEMS     = 1,
   RESERVE_CARD  = 2
  };

  /**
   * The location from which a card is being used
   */
  enum CardLocation
  {
   TIER_1   = 0,
   TIER_2   = 1,
   TIER_3   = 2,
   RESERVED = 3
  };
  
} // namespace splendor

#endif // SPLENDOR_ENUMS_H
