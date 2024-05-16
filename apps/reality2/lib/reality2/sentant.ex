defmodule Reality2.Sentant do
# *******************************************************************************************************************************************
@moduledoc false
# Start the Sentant, which is a Supervisor that manages the Sentant's Automations, Comms and Plugins.
#
# **Author**
# - Dr. Roy C. Davies
# - [roycdavies.github.io](https://roycdavies.github.io/)
# *******************************************************************************************************************************************

  use Supervisor, restart: :transient
  alias Reality2.Helpers.R2Process, as: R2Process

  # -----------------------------------------------------------------------------------------------------------------------------------------
  # Supervisor Callbacks
  # -----------------------------------------------------------------------------------------------------------------------------------------
  @doc false
  def start_link({name, id, sentant_map}) do
    new_sentant_map = Map.merge(sentant_map, %{"id" => id, "name" => name})
    Supervisor.start_link(__MODULE__, {name, id, new_sentant_map})
    |> R2Process.register(id)
  end

  @impl true
  def init({name, id, sentant_map}) do
    children = [
      {Reality2.Plugins, {name, id, sentant_map}},
      {Reality2.Automations, {name, id, sentant_map}},
      {Reality2.Sentant.Comms, {name, id, sentant_map}}
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end
  # -----------------------------------------------------------------------------------------------------------------------------------------



  # -----------------------------------------------------------------------------------------------------------------------------------------
  # Public Functions
  # -----------------------------------------------------------------------------------------------------------------------------------------

  # -----------------------------------------------------------------------------------------------------------------------------------------



  # -----------------------------------------------------------------------------------------------------------------------------------------
  # Helper Functions
  # -----------------------------------------------------------------------------------------------------------------------------------------

  # -----------------------------------------------------------------------------------------------------------------------------------------
end